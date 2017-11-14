#!/bin/sh
. shell/settings.sh
. shell/menu/common.sh
. shell/menu/stream/audio.sh

change_stream_uri() {
    prompt="Enter stream URI.\nAssumes local path if no protocol specified."

    show_window \
        --title "Stream URI" \
        --inputbox "$prompt" \
        $(height) $(width) \
        "$streamuri"

    if [ "$?" -eq 0 ]; then
        set_data streamuri "$(get_result)"
    fi
}

change_stream_dest() {
    prompt="Enter stream endpoint (e.g., filename, RTMP key).\n\nIf streaming to Twitch, enter the RTMP key found in your account's dashboard. It should begin with \"live\".\nIf streaming to a file, make sure the extension matches the output format in shell/core/stream.sh"

    show_window \
        --title "Stream Destination" \
        --inputbox "$prompt" \
        $(height) $(width) \
        "$streamdest"

    if [ "$?" -eq 0 ]; then
        set_data streamdest "$(get_result)"
    fi
}

change_stream_loop() {
    if $streamloops; then
        default=
    else
        default="--defaultno"
    fi

    prompt="Enable stream looping? This will make the stream restart instead of terminating once the end of the stream audio file is reached. If the stream uses emulator audio, setting this option does nothing."

    whiptail \
        --title "Stream Loop" $default \
        --yesno "$prompt" \
        $(height) $(width)

    if [ "$?" -eq 0 ]; then
        set_data streamloops "true"
    else
        set_data streamloops "false"
    fi
}

change_stream_signal() {
    if $streamsig; then
        default=
    else
        default="--defaultno"
    fi

    prompt="Enable end-of-stream signal? This will send a SIGALRM to the Twitch bot's process every time the stream restarts."

    whiptail \
        --title "Stream Signal" $default \
        --yesno "$prompt" \
        $(height) $(width)

    if [ "$?" -eq 0 ]; then
        set_data streamsig "true"
    else
        set_data streamsig "false"
    fi
}

stream_menu() {
    status=0

    while [ "$status" -eq 0 ]; do
        show_window \
            --title "Stream" --notags \
            --menu "Configure which option?" \
            $(height) $(width) 5 \
            1 "Audio" \
            2 "Looping" \
            3 "End-of-Stream Signal" \
            4 "Stream URI" \
            5 "Stream Endpoint"
        status=$?

        case "$(get_result)" in
            1)
                audio_menu
                ;;
            2)
                change_stream_loop
                ;;
            3)
                change_stream_signal
                ;;
            4)
                change_stream_uri
                ;;
            5)
                change_stream_dest
                ;;
        esac
    done

    main_menu
}
