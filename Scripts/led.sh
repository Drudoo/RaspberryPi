#/bin/bash
LEDPin=$1
gpio mode $LEDPin output

is_off ()
{
       return $(gpio read $LEDPin);
}

case $2 in
        off)
                gpio write $LEDPin 0
        ;;
        on)
                if is_off; then
                        gpio write $LEDPin 1
                else
                        echo "led is on"
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