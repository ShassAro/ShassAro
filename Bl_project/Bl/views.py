from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from serializers import *
from models import *
from create_game import *


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class LearningPathViewSet(ModelViewSet):
    queryset = LearningPath.objects.all()
    serializer_class = LearningPathSerializer


class GameUserViewSet(ModelViewSet):
    queryset = GameUser.objects.all()
    serializer_class = GameUserSerializer


class ShassaroViewSet(ModelViewSet):
    queryset = Shassaro.objects.all()
    serializer_class = ShassaroSerializer


class GameViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def create(self, request, *args, **kwargs):
        """
        :param request: data is expected to be in the format of:
        {
            participants:{
                group1: ["assaf", "roi"],
                group2: ["shay", "abbale"]
            },
            images: [
                {image1},
                {image2}
            ]
        }
        :return: a new game
        """
        try:
            # parse request payload
            participants = request.data["participants"]
            images = request.data["images"]

            # build a game instance
            game = Game()
            for participant, image in (participants, images):
                shassaro = generate_initial_shassaro(participant, image)
                game.shassaros.add(shassaro)

            # deploy the shassaros
            game.shassaros = deploy_shassaros(game.shassaros)

            # save to db and return
            game.save()
            return Response(data=game, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(data=e.__dict__, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GameResultViewSet(ModelViewSet):
    queryset = GameResult.objects.all()
    serializer_class = GameResultSerializer


class BadgeViewSet(ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer


class DockerServerViewSet(ModelViewSet):
    queryset = DockerServer.objects.all()
    serializer_class = DockerServerSerializer


class ConfigurationsViewSet(ModelViewSet):
    queryset = Configurations.objects.all()
    serializer_class = ConfigurationsSerializer
