import controller
command = "create playlist"
arg1 = "testing"
arg2 = ""
arg3 = ""
arg4 = ""
if command == "play":
    controller.playSong()

elif command == "pause":
    controller.pauseSong()

elif command == "skip":
    controller.skipSong()

elif command == "previous":
    controller.previousSong()

elif command == "shuffle on":
    controller.shuffle(True)

elif command == "shuffle off":
    controller.shuffle(False)
    
elif command == "repeat on":
    controller.repeat(True)

elif command == "repeat off":
    controller.repeat(False)

elif command == "seek to ":
    controller.seekTo(arg1)

elif command == "create playlist":
    if arg1 != "":
        if arg2 == "" and arg3 == "":
            controller.createPlaylist(arg1, False, False, arg4)
        elif arg2 == "":
            controller.createPlaylist(arg1, False, arg3, arg4)
        elif arg3 == "":
            controller.createPlaylist(arg1, arg2, False, arg4)
        else:
            controller.createPlaylist(arg1, arg2, arg3, arg4)