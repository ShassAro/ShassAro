from models import *
import socket
import fcntl
import struct

# Magic. Don't touch.
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,         # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

# Initialize all test data
def init_data():

    ### Create Tags ###
    tag_mysql = Tag(name="MySQL", description="Images that require knowledge in MySQL.")
    tag_mysql.save()
    tag_php = Tag(name="PHP", description="Images that require knowledge in PHP.")
    tag_php.save()
    tag_bash = Tag(name="Bash", description="Images that require knowledge in Bash.")
    tag_bash.save()
    tag_apache = Tag(name="Apache", description="Images that require knowledge in Apache.")
    tag_apache.save()
    tag_ftp = Tag(name="FTP", description="Images that require knowledge in FTP.")
    tag_ftp.save()
    tag_social = Tag(name="Social", description="Images that require some social engineering.")
    tag_social.save()
    tag_poc = Tag(name="POC", description="Images that require no knowledge.")
    tag_poc.save()

    ### Create Statuses ###
    status = GameRequestStatus(status="WAITING", message="Waiting for another player...")
    status.save()
    status = GameRequestStatus(status="DEPLOYING", message="Found a player, creating a game")
    status.save()
    status = GameRequestStatus(status="DONE", message="Challenge accepted!")
    status.save()
    status = GameRequestStatus(status="ERROR", message="Sorry... no challenges for you today :(")
    status.save()

    ### Create Image object for Challenge1 ###
    img_challenge1 = Image(docker_name="shassaro/challenge1", description="POC image", level=1, allow_in_game=True, goal_description=['tahat','another-tahat'], hints=["Try to tahat (not too much tahat)", "Keep that in mind. Tahat is the shit."], duration_minutes=60)
    img_challenge1.save()
    img_challenge1.tags.add(tag_poc)
    img_challenge1.save()

    ### Create Image object for Challenge2 ###
    img_challenge2 = Image(docker_name="shassaro/challenge2", description="Reverse shell", level=1, allow_in_game=True, hints=["The bash version have not been updated in a while..", "Look at the website source.."], goal_description=['Find reverse shell!','Get the secret from the DB'], duration_minutes=60)
    img_challenge2.save()
    img_challenge2.tags.add(tag_bash)
    img_challenge2.tags.add(tag_apache)
    img_challenge2.tags.add(tag_mysql)
    img_challenge2.save()

    ### Create Image object for Challenge3 ###
    img_challenge3 = Image(docker_name="shassaro/challenge3", description="FTP and Apache", level=1, allow_in_game=True, hints=["Can you login to the FTP server", "HTML is the source of all evil"], goal_description=['Get into the FTP server', 'Find the secret'], duration_minutes=60)
    img_challenge3.save()
    img_challenge3.tags.add(tag_ftp)
    img_challenge3.tags.add(tag_social)
    img_challenge3.save()

    # Get eth0's IP address
    own_ip = get_ip_address('eth0')

    ### Create object for Docker Server ###
    docker_server = DockerServer(name="primary", protocol="http", ip=own_ip, port="4243")
    docker_server.save()

    ### Create object for Docker Manager ###
    docker_mgr = DockerManager(name="docker-manager", ip=own_ip, port="8000")
    docker_mgr.save()

    ### Create user objects ###
    for i in ["shay", "assaf", "roi", "sheker", "beker", "bla", "tahat", "tusik"]:
        temp = User(username=i, email="{0}@shassaro.com".format(i), first_name=i, last_name="lastname")
        temp.set_password("123456")
        temp.save()

    ### Create quotes ###
    quote = Quotes(quote="When Life Gives You Questions, Google has Answers.")
    quote.save()
    quote = Quotes(quote="My pokemon brings all the nerds to the yard, and they're like you wanna trade cards? Darn right, I wanna trade cards, I'll trade this but not my charizard.")
    quote.save()
    quote = Quotes(quote="1f u c4n r34d th1s u r34lly n33d t0 g37 l41d.")
    quote.save()
    quote = Quotes(quote="If at first you don't succeed; call it version 1.0.")
    quote.save()
    quote = Quotes(quote="I'm not anti-social; I'm just not user friendly.")
    quote.save()
    quote = Quotes(quote="I would love to change the world, but they won't give me the source code.")
    quote.save()
    quote = Quotes(quote="Artificial Intelligence is no match for Natural Stupidity.")
    quote.save()
    quote = Quotes(quote="A computer lets you make more mistakes faster than any invention in human history - with the possible exceptions of handguns and tequila.")
    quote.save()
    quote = Quotes(quote="People say that if you play Microsoft CD's backwards, you hear satanic things, but that's nothing, because if you play them forwards, they install Windows.")
    quote.save()
    quote = Quotes(quote="In a world without fences and walls, who needs Gates and Windows?")
    quote.save()
    quote = Quotes(quote="My software never has bugs. It just develops random features.")
    quote.save()
    quote = Quotes(quote="Girls are like internet domain names, the ones I like are already taken.")
    quote.save()
    quote = Quotes(quote="Software is like sex: It's better when it's free.")
    quote.save()
    quote = Quotes(quote="COFFEE.EXE Missing - Insert Cup and Press Any Key.")
    quote.save()
    quote = Quotes(quote="Who is General Failure and why is he reading my disk?")
    quote.save()
    quote = Quotes(quote="The difference between e-mail and regular mail is that computers handle e-mail, and computers never decide to come to work one day and shoot all the other computers (yet).")
    quote.save()
    quote = Quotes(quote="User Error. Please replace user and press any key to continue.")
    quote.save()
    quote = Quotes(quote="'be strong', I whispered to my WiFi signal.")
    quote.save()
    quote = Quotes(quote="Programmers are tools for converting caffeine into code.")
    quote.save()
    quote = Quotes(quote="See daddy ? All the keys are in alphabetical order now.")
    quote.save()
    quote = Quotes(quote="Yo moma is like HTML: Tiny head, huge body.")
    quote.save()
    quote = Quotes(quote="The more I C, the less I see.")
    quote.save()
    quote = Quotes(quote="The only problem with troubleshooting is that sometimes trouble shoots back.")
    quote.save()
    quote = Quotes(quote="rm -rf /bin/laden")
    quote.save()
    quote = Quotes(quote="Programming is like sex, one mistake and you have to support it for the rest of your life.")
    quote.save()
    quote = Quotes(quote="I think Microsoft named .Net so it would not show up in a Unix directory listing.")
    quote.save()
    quote = Quotes(quote="Hardware: The parts of a computer system that can be kicked.")
    quote.save()