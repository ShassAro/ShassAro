from datetime import datetime, timedelta, date
from django.shortcuts import redirect
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from generate_active_game import GenerateActiveGame
from end_game import end_game
from scavage import scavage
from forfeit import forfeit
from serializers import *
from models import *
from create_game import *
from django.db.models import Q
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
import logging

logger = logging.getLogger(__name__)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAdminUser,)


class LearningPathViewSet(ModelViewSet):
    queryset = LearningPath.objects.all()
    serializer_class = LearningPathSerializer
    permission_classes = (permissions.IsAdminUser,)


class GameUserViewSet(ModelViewSet):
    queryset = GameUser.objects.all()
    serializer_class = GameUserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ShassaroViewSet(ModelViewSet):
    queryset = Shassaro.objects.all()
    serializer_class = ShassaroSerializer
    permission_classes = (permissions.IsAdminUser,)


class GameRequestStatuses:
    def __init__(self):
        pass

    WAITING = "WAITING"
    DEPLOYING = "DEPLOYING"
    DONE = "DONE"
    ERROR = "ERROR"


class GameRequestViewSet(ModelViewSet):
    queryset = GameRequest.objects.all()
    serializer_class = GameRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_a_game_request_status(self, status):
        return GameRequestStatus.objects.get(status=status)

    def pick_best_image(self, tags_user1, tags_user2):

        queries = [Q(tags__name=value.name) for value in tags_user1.all()]
        query = queries.pop()

        for item in queries:
            query |= item

        # User 1 tags defines user 2 image
        user2_image = Image.objects.filter(query).order_by("?").first()

        queries = [Q(tags__name=value.name) for value in tags_user2.all()]
        query = queries.pop()

        for item in queries:
            query |= item

        # User 1 tags defines user 2 image
        user1_image = Image.objects.filter(query).order_by("?").first()


        return (user1_image.docker_name, user2_image.docker_name)

    def create(self, request, *args, **kwargs):

        try:
            # Get username and verify it exists
            username = request.DATA["username"]
            user_object = User.objects.filter(username=username)
            if len(user_object) == 0:
                return Response(data="Username does not exist.", status=status.HTTP_400_BAD_REQUEST)

            tags = request.DATA.getlist("tags")

            logger.debug("Got a game request for user {0}".format(username))

        except Exception as e:
            return Response(data=e.__dict__, status=status.HTTP_400_BAD_REQUEST)

        try:

            tag_objects = [Tag.objects.get(name=tag.split('/')[-2]) for tag in tags]
            game_request = GameRequest(
                username=username,
                submitted_at=datetime.now().replace(tzinfo=None))

            game_request.status = self.get_a_game_request_status(GameRequestStatuses.WAITING)
            for tag in tag_objects:
                game_request.tags.add(tag)

            game_request.save()

            # Notify via websocket
            user_publisher = RedisPublisher(facility=username, broadcast=True)
            user_publisher.publish_message(RedisMessage(serializers.serialize("json",[game_request])))

            # Do we have another user? (that's not us..)

            match = GameRequest.objects.\
                filter(status=GameRequestStatus.objects.get(status=GameRequestStatuses.WAITING)).\
                exclude(username=username).order_by("submitted_at")

            if (len(match) == 0):

                logger.debug("No match found.. waiting for next player.")
                return Response(data=serializers.serialize("json",[game_request]), status=status.HTTP_201_CREATED)

            match = match[0]
            logger.debug("Found match! competing with: {0}".format(match.username))

            # Lets create websockets endpoint so we can communicate with the remote user also
            remote_user_publisher = RedisPublisher(facility=match.username, broadcast=True)

            logger.debug("Picking up images..")

            # Get the images
            picked_images = [Image.objects.get(docker_name=image_name) for
                             image_name in self.pick_best_image(game_request.tags, match.tags)]

            logger.debug("Done picking images.")

            game_request.status = self.get_a_game_request_status(GameRequestStatuses.DEPLOYING)
            match.status = self.get_a_game_request_status(GameRequestStatuses.DEPLOYING)
            game_request.save()
            match.save()

            logger.debug("Mark both requests as deploying.")

            # Now we need to notify the users that we have found them a user, and their status is deploying
            user_publisher.publish_message(RedisMessage(serializers.serialize("json",[game_request])))
            remote_user_publisher.publish_message(RedisMessage(serializers.serialize("json",[match])))

            logger.debug("Notifyed users via websockets.")

            logger.debug("Start with create game routine.")
            created_game = CreateGame.create([username, match.username], picked_images)

            logger.debug("Done with create game! notify as done.")
            game_request.status = self.get_a_game_request_status(GameRequestStatuses.DONE)
            match.status = self.get_a_game_request_status(GameRequestStatuses.DONE)
            game_request.save()
            match.save()

            game_request.game.add(created_game)
            match.game.add(created_game)
            game_request.save()
            match.save()

            logger.debug("Marked the objects as done and attached the game.")

            # And notify that its done
            user_publisher.publish_message(RedisMessage(serializers.serialize("json",[game_request])))
            remote_user_publisher.publish_message(RedisMessage(serializers.serialize("json",[match])))

            logger.debug("Notified via websockets that the gamerequest is done")

            # Now, we need to create another websocket to let the web know about the active game
            user_publisher = RedisPublisher(facility="{0}-game".format(username), broadcast=True)
            remote_user_publisher = RedisPublisher(facility="{0}-game".format(match.username), broadcast=True)

            logger.debug("2nd websockets created")

            user_publisher.publish_message(RedisMessage(json.dumps(GenerateActiveGame(username))))
            remote_user_publisher.publish_message(RedisMessage(json.dumps(GenerateActiveGame(match.username))))

            logger.debug("Notified the new websocket about the active game.")

            logger.debug("GAME REQUEST ALL DONE")
            return Response(data=serializers.serialize("json",[game_request]), status=status.HTTP_201_CREATED)

        except Exception as e:
            try:
                game_request.status = self.get_a_game_request_status(GameRequestStatuses.ERROR)
                game_request.save()
                match.status = self.get_a_game_request_status(GameRequestStatuses.ERROR)
                match.save()

                # Notify both users about an error
                user_publisher.publish_message(RedisMessage(serializers.serialize("json",[game_request])))
                remote_user_publisher.publish_message(RedisMessage(serializers.serialize("json",[match])))

                # And delete the objects..
                game_request.delete()
                match.delete()

            except Exception as inner:
                pass
            return Response(data=e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GameRequestStatusViewSet(ModelViewSet):
    queryset = GameRequestStatus.objects.all()
    serializer_class = GameRequestStatusSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CreateGameError(Exception):
    pass


class CreateGame():
    @staticmethod
    def create(participants, images):
        try:

            logger.debug("Building a game object")

            # build a game instance
            game = Game.objects.create()
            for i in range(2):
                shassaro = generate_initial_shassaro(participants[i], images[i])
                game.shassaros.add(shassaro)
                game.images.add(images[i])

            logger.debug("Game objects build!")

            logger.debug("Start with the deploy.")

            # deploy the shassaros
            deploy_shassaros(game.shassaros.all())

            logger.debug("Done deploying!")

            logger.debug("Start to fill the game object.")

            # Fill out game
            game.start_time = datetime.now().replace(tzinfo=None)
            game.userA = participants[0]
            game.userB = participants[1]

            # Fill duration_minutes
            game_duration_minutes = 0
            for image in images:
                if image.duration_minutes > game_duration_minutes:
                    game_duration_minutes = image.duration_minutes
            game.duration_minutes = game_duration_minutes

            # save to db and return
            game.save()

            logger.debug("All done with filling the game object.")

            return game

        except Exception as e:
            if game is not None:
                if game.shassaros is not None:
                    for shassaro in game.shassaros.all():
                        shassaro.delete()
                game.delete()
            raise CreateGameError(e)


class GameViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (permissions.IsAuthenticated,)


class GameResultViewSet(ModelViewSet):
    queryset = GameResult.objects.all()
    serializer_class = GameResultSerializer
    permission_classes = (permissions.IsAuthenticated,)


class BadgeViewSet(ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = (permissions.IsAuthenticated,)


class DockerManagerViewSet(ModelViewSet):
    queryset = DockerManager.objects.all()
    serializer_class = DockerManagerSerializer
    permission_classes = (permissions.IsAdminUser,)


class DockerServerViewSet(ModelViewSet):
    queryset = DockerServer.objects.all()
    serializer_class = DockerServerSerializer
    permission_classes = (permissions.IsAdminUser,)




class ActiveGameGoalCheckViewSet(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kw):

        # Get the username from GET
        username = kw["username"]
        user_index = 0

        # Get the game object. Try userA first.
        gameObj = Game.objects.filter(userA=username)

        if (len(gameObj) == 0):

            # Lets try userB
            gameObj = Game.objects.filter(userB=username)
            user_index = 1

        # If none found -> game is over. return gameresult.
        if (len(gameObj) == 0):

            returnJson = {
                "status" : False,
                "all_completed" : False
            }

            # Redirect to gameresult to the last game of all
            return Response(returnJson, status=status.HTTP_200_OK)

        try:
            goal_hash = request.GET["hash"]
        except:
            return Response("Expecting querystring named hash.. /?hash=1234")

        found = False
        finished = False

        # We need to cross the users goals check.
        user_index = abs(user_index-1)

        for goal in gameObj[0].shassaros.all()[user_index].goals:
            if (goal_hash == goal):

                currShassaro = gameObj[0].shassaros.all()[user_index]
                if (currShassaro.goals_completed == None):

                    currShassaro.goals_completed = {goal : True}
                    found = True

                else:
                    goalAdded = None
                    for currIndex in currShassaro.goals_completed:
                        if (goal != currIndex):
                            goalAdded = goal
                            found = True

                    if (goalAdded != None):
                        currShassaro.goals_completed[goal] = True

                currShassaro.save()

                if (len(currShassaro.goals_completed) == len(gameObj[0].shassaros.all()[user_index].goals)):

                    other_username = None

                    # And cross it back to original
                    user_index = abs(user_index-1)

                    if(user_index == 0):
                        other_username = gameObj[0].userB
                    else:
                        other_username = gameObj[0].userA



                    end_game(gameObj[0], username, other_username)
                    finished = True

        if(found):

            # Notify change via websockets
            userA_publisher = RedisPublisher(facility="{0}-game".format(gameObj[0].userA), broadcast=True)
            userB_publisher = RedisPublisher(facility="{0}-game".format(gameObj[0].userB), broadcast=True)

            userA_publisher.publish_message(RedisMessage(json.dumps(GenerateActiveGame(gameObj[0].userA))))
            userB_publisher.publish_message(RedisMessage(json.dumps(GenerateActiveGame(gameObj[0].userB))))

        returnJson = {
            "status" : found,
            "all_completed" : finished
        }

        return Response(returnJson, status=status.HTTP_200_OK)


class ScavageViewSet(APIView):

    permission_classes = (permissions.IsAdminUser,)

    @staticmethod
    def post(self):

        response = scavage()
        return response


class ForfeitViewSet(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def post(self, request, *args, **kwargs):

        try:
            username = request.DATA['username']
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            response = forfeit(username=username)
            return response

        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ActiveGameViewSet(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kw):

        # Get the username from GET
        username = kw["username"]

        returnJson = GenerateActiveGame(username)

        return Response(returnJson, status=status.HTTP_200_OK)


class UserList(ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    lookup_field = "username"
    queryset = User.objects.all()


class UserRegisterViewSet(APIView):

    def post(self, request, *args, **kw):

        try:
            username = request.DATA['username']
            password = request.DATA['password']
            email = request.DATA['email']
            first_name = request.DATA['first_name']
            last_name = request.DATA['last_name']

        except Exception as e:
            return Response("Accepted json fields: username, password, email, first_name, last_name", status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User()
            user.username = username
            user.set_password(password)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            return Response("User created! Gotta Beat Them'all!", status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(data=e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class QuotesViewSet(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kw):
        quote = Quotes.objects.order_by("?").first()
        return Response(quote.quote, status=status.HTTP_200_OK)


class QuietBasicAuthentication(BasicAuthentication):
    # disclaimer: once the user is logged in, this should NOT be used as a
    # substitute for SessionAuthentication, which uses the django session cookie,
    # rather it can check credentials before a session cookie has been granted.
    def authenticate_header(self, request):
        return 'xBasic realm="%s"' % self.www_authenticate_realm


class ValidateToken(APIView):

    def post(self, request, *args, **kwargs):

        try:
            token_key = request.DATA['token']
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            if len(Token.objects.filter(key=token_key)) != 0:  # Token is valid
                return Response(data=True, status=status.HTTP_200_OK)
            else:
                return Response(data=False, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AuthView(APIView):
    authentication_classes = (QuietBasicAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        if (len(Token.objects.filter(user=request.user)) == 0):
            token = Token.objects.create(user=request.user)
        else:
            token = Token.objects.filter(user=request.user).first()

        returnJson = {
            "token" : token.key,
            "username" : request.user
        }

        return Response(returnJson, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):

        Token.objects.filter(user=request.user).delete()
        return Response("You are done motherfucker", status=status.HTTP_200_OK)


class LogoutView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):

        Token.objects.filter(user=request.user).delete()
        return Response("You are done motherfucker", status=status.HTTP_200_OK)


class UserStatsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        username = kwargs["username"]

        gameresults = GameResult.objects.filter(Q(winning_users=User.objects.filter(username=username)) |
                                                Q(losing_users=User.objects.filter(username=username)))

        wingameresult = GameResult.objects.filter(winning_users=User.objects.filter(username=username))

        yesterday = date.today() - timedelta(days=1)

        total_games = len(gameresults)
        total_wins = len(wingameresult)
        games_today = len(gameresults.filter(start_time__gt=yesterday))
        wins_today = len(wingameresult.filter(start_time__gt=yesterday))

        resultJson = {
            "total_games" : total_games,
            "total_wins" : total_wins,
            "games_today" : games_today,
            "win_today" : wins_today
        }

        return Response(resultJson, status=status.HTTP_200_OK)

