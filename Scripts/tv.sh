#/bin/bash

is_off ()
{
        status=$(echo pow 0 | cec-client -s -d 1 | grep "power status: " | sed 's/^.*: //')
        if [ $status = 'on' ]; then
                return 1
        else
                return 0
        fi
}

case $1 in
        off)
               echo standby 0 | cec-client -s -d 1 > /dev/null
        ;;
        on)
                if is_off; then
                        echo on 0 | cec-client -s -d 1
                else
                        echo "TV is on"
                fi
        ;;
        status)
                if is_off; then
                        echo "OFF"
                else
                        echo "ON"
                fi
        ;;
esac