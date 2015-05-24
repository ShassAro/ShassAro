from datetime import datetime
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from end_game import end_game
from serializers import *
from models import *
from create_game import *
from django.db.models import Q
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage


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
    permission_classes = (permissions.IsAuthenticated,)


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
        return ("shassaro/challenge1", "shassaro/challenge1")

    def create(self, request, *args, **kwargs):

        try:
            username = request.DATA["username"]
            tags = request.DATA.getlist("tags")

        except Exception as e:
            return Response(data=e.__dict__, status=status.HTTP_400_BAD_REQUEST)

        try:

            tag_objects = [Tag.objects.get(name=tag.split('/')[-2]) for tag in tags]
            game_request = GameRequest(
                username=username,
                submitted_at=datetime.now())

            game_request.status = self.get_a_game_request_status(GameRequestStatuses.WAITING)
            for tag in tag_objects:
                game_request.tags.add(tag)

            game_request.save()


            # Notify via websocket
            user_publisher = RedisPublisher(facility=username, broadcast=True)
            user_publisher.publish_message(RedisMessage(serializers.serialize("json",[game_request])))

            # Do we have another user? (thats not us..)

            match = GameRequest.objects.\
                filter(status=GameRequestStatus.objects.get(status=GameRequestStatuses.WAITING)).\
                exclude(username=username)

            if (len(match) == 0):

                return Response(data=serializers.serialize("json",[game_request]), status=status.HTTP_201_CREATED)

            match = match[0]

            # Lets create websockets endpoint so we can communicate with the remote user also
            remote_user_publisher = RedisPublisher(facility=match.username, broadcast=True)

            # Get the images
            picked_images = [Image.objects.get(docker_name=image_name) for
                             image_name in self.pick_best_image(tags, match.tags)]


            game_request.status = self.get_a_game_request_status(GameRequestStatuses.DEPLOYING)
            match.status = self.get_a_game_request_status(GameRequestStatuses.DEPLOYING)
            game_request.save()
            match.save()

            # Now we need to notify the users that we have found them a user, and their status is deploying
            user_publisher.publish_message(RedisMessage(serializers.serialize("json",[game_request])))
            remote_user_publisher.publish_message(RedisMessage(serializers.serialize("json",[match])))

            created_game = CreateGame.create([username, match.username], picked_images)

            game_request.status = self.get_a_game_request_status(GameRequestStatuses.DONE)
            match.status = self.get_a_game_request_status(GameRequestStatuses.DONE)
            game_request.save()
            match.save()

            game_request.game.add(created_game)
            match.game.add(created_game)
            game_request.save()
            match.save()

            # And notify that its done
            user_publisher.publish_message(RedisMessage(serializers.serialize("json",[game_request])))
            remote_user_publisher.publish_message(RedisMessage(serializers.serialize("json",[match])))

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

            # build a game instance
            game = Game.objects.create()
            for i in range(2):
                shassaro = generate_initial_shassaro(participants[i], images[i])
                game.shassaros.add(shassaro)
                game.images.add(images[i])

            # deploy the shassaros
            deploy_shassaros(game.shassaros.all())

            # Fill out game
            game.start_time = datetime.now()
            game.userA = participants[0]
            game.userB = participants[1]

            # save to db and return
            game.save()
            return game

        except Exception as e:
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


class ConfigurationsViewSet(ModelViewSet):
    queryset = Configurations.objects.all()
    serializer_class = ConfigurationsSerializer
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

                    if(user_index == 0):
                        other_username = gameObj[0].userB
                    else:
                        other_username = gameObj[0].userA

                    end_game(gameObj[0], username, other_username)
                    finished = True

        returnJson = {
            "status" : found,
            "all_completed" : finished
        }

        return Response(returnJson, status=status.HTTP_200_OK)

class ActiveGameViewSet(APIView):

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

            # Find all game result that the user is a member of
            allGames = GameResult.objects.filter(Q(losing_users__username=username  ) | Q(winning_users__username=username))

            # Redirect to gameresult to the last game of all
            return redirect("/game_results/{0}".format(allGames.order_by("-start_time")[0].pk), permanent=False)

        # Assume two user have different images
        image_index = user_index

        # Find out if the users uses the same image
        if (len(gameObj[0].images.all()) == 1):
            image_index = 0 # Force the usage of the first image

        returnJson = {
            "username" : gameObj[0].shassaros.all()[user_index].participants.all()[0].name,
            "vnc_port" : gameObj[0].shassaros.all()[user_index].participants.all()[0].vnc_port,
            "password" : gameObj[0].shassaros.all()[user_index].participants.all()[0].password,
            "goals" : gameObj[0].images.all()[image_index].goal_description,
            "hints" : gameObj[0].images.all()[image_index].hints,
            "duration" : gameObj[0].images.all()[image_index].duration_minutes,
            "start_time" :gameObj[0].start_time,
            "remote_ip" : gameObj[0].shassaros.all()[abs(user_index-1)].shassaro_ip,
            "docker_manager_ip": DockerManager.objects.first().ip
        }

        return Response(returnJson, status=status.HTTP_200_OK)


class UserList(ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserRegisterViewSet(APIView):

    def post(self, request, *args, **kw):

        try:
            username = request.DATA['username']
            password = request.DATA['password']
            email = request.DATA['email']

        except Exception as e:
            return Response("Accepted json fields: username, password, email", status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User()
            user.username = username
            user.set_password(password)
            user.email = email
            user.save()

            return Response("User created! Gotta Beat Them'all!", status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(data=e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class QuotesViewSet(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kw):
        quote = Quotes.objects.order_by("?").first()
        return Response(quote.quote, status=status.HTTP_200_OK)