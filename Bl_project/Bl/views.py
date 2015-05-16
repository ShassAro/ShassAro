from datetime import datetime
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from end_game import end_game
from serializers import *
from models import *
from create_game import *
from django.db.models import Q

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAdminUser,)


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
    permission_classes = (permissions.IsAdminUser,)


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

            # Do we have another user? (thats not us..)

            match = GameRequest.objects.\
                filter(status=GameRequestStatus.objects.get(status=GameRequestStatuses.WAITING)).\
                exclude(username=username)

            if (len(match) == 0):
                return Response(data=serializers.serialize("json",[game_request]), status=status.HTTP_201_CREATED)

            match = match[0]

            # Get the images
            picked_images = [Image.objects.get(docker_name=image_name) for
                             image_name in self.pick_best_image(tags, match.tags)]


            game_request.status = self.get_a_game_request_status(GameRequestStatuses.DEPLOYING)
            match.status = self.get_a_game_request_status(GameRequestStatuses.DEPLOYING)
            game_request.save()
            match.save()

            created_game = CreateGame.create([username, match.username], picked_images)

            game_request.status = self.get_a_game_request_status(GameRequestStatuses.DONE)
            match.status = self.get_a_game_request_status(GameRequestStatuses.DONE)
            game_request.save()
            match.save()

            game_request.game.add(created_game)
            match.game.add(created_game)
            game_request.save()
            match.save()

            return Response(data=serializers.serialize("json",[game_request]), status=status.HTTP_201_CREATED)

        except Exception as e:
            try:
                game_request.status = self.get_a_game_request_status(GameRequestStatuses.ERROR)
                game_request.save()
            except Exception as inner:
                pass
            return Response(data=e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GameRequestStatusViewSet(ModelViewSet):
    queryset = GameRequestStatus.objects.all()
    serializer_class = GameRequestStatusSerializer


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
    permission_classes = (permissions.IsAdminUser,)


class GameResultViewSet(ModelViewSet):
    queryset = GameResult.objects.all()
    serializer_class = GameResultSerializer
    permission_classes = (permissions.IsAdminUser,)


class BadgeViewSet(ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = (permissions.IsAdminUser,)


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


class ActiveGameViewSet(APIView):

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
            return redirect("/game_results/{0}".format(allGames.order_by("-start_time")[0].pk))

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