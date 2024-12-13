import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 600
    height: 400
    color: "#191414"
    property bool isOn: false   

    Image {
        id: button
        width: 100
        height: 100
        anchors.centerIn: parent
        source: isOn ? "on.svg" : "off.svg"
        scale: 1.0
        
        SequentialAnimation {
            id: pulseAnimation
            running: false  // Initially, the animation is not running
            loops: Animation.Infinite
            
            NumberAnimation {
                target: button
                property: "scale"
                from: 1.0
                to: 1.2
                duration: 500
                easing.type: Easing.InOutQuad
            }
            NumberAnimation {
                target: button
                property: "scale"
                from: 1.2
                to: 1.0
                duration: 500
                easing.type: Easing.InOutQuad
            }
        }
        
        Timer {
            id: pulseDelayTimer
            interval: 1000  // 1-second delay
            repeat: false
            onTriggered: pulseAnimation.start()
        }
        
        MouseArea {
            anchors.fill: parent
            onClicked: {
                isOn = !isOn
                if (isOn) { 
                    programRunner.run_program();
                    pulseDelayTimer.start();  // Start the delay timer
                } else {
                    pulseAnimation.stop();
                    button.scale = 1.0;
                    programRunner.stop_program();
                }
            }
        }
    }
}

