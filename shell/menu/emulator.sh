#!/bin/sh
. shell/settings.sh
. "$shldir/tests.sh"
. "$shldir/menu/common.sh"

change_rom_dir() {
    update_data emurom
    default=$(get_default_dir "$emurom")

    show_window -sl inputbox \
        -t "ROM Location" \
        -p "Enter location of the ROM (must be compatible with the emulator):" \
        -- "$default"

    if [ $? -eq 0 ]; then
        set_file emurom "$(get_result)"
        check_file_error
    fi

    emulator_menu
}

emulator_menu() {
    show_window -sl menu \
        -t "Emulator" \
        -p "Configure which option?" \
        -- 1 \
        1 "ROM Location"

    if [ $? -eq 0 ]; then
        case "$(get_result)" in
            1)
                change_rom_dir
                ;;
        esac
    fi

    main_menu
}
