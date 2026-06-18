#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <time.h>

#include <sys/socket.h>
#include <linux/can.h>
#include <linux/can/raw.h>
#include <net/if.h>
#include <sys/ioctl.h>

#define SPEED_ID 0x100
#define RPM_ID   0x101

int main() {

    int socket_fd;
    struct sockaddr_can addr;
    struct ifreq ifr;

    socket_fd = socket(
        PF_CAN,
        SOCK_RAW,
        CAN_RAW
    );

    strcpy(
        ifr.ifr_name,
        "vcan0"
    );

    ioctl(
        socket_fd,
        SIOCGIFINDEX,
        &ifr
    );

    addr.can_family = AF_CAN;
    addr.can_ifindex = ifr.ifr_ifindex;

    bind(
        socket_fd,
        (struct sockaddr *)&addr,
        sizeof(addr)
    );

    srand(time(NULL));

    int speed = 60;
    int rpm = 2500;

    printf("[+] C Engine ECU Started\n");

    while (1) {

        speed += (rand() % 5) - 2;
        rpm += (rand() % 201) - 100;

        if (speed < 0)
            speed = 0;

        if (rpm < 700)
            rpm = 700;

        struct can_frame speed_frame;

        speed_frame.can_id = SPEED_ID;
        speed_frame.can_dlc = 2;

        speed_frame.data[0] =
            (speed >> 8) & 0xFF;

        speed_frame.data[1] =
            speed & 0xFF;

        write(
            socket_fd,
            &speed_frame,
            sizeof(speed_frame)
        );

        struct can_frame rpm_frame;

        rpm_frame.can_id = RPM_ID;
        rpm_frame.can_dlc = 2;

        rpm_frame.data[0] =
            (rpm >> 8) & 0xFF;

        rpm_frame.data[1] =
            rpm & 0xFF;

        write(
            socket_fd,
            &rpm_frame,
            sizeof(rpm_frame)
        );

        printf(
            "[C Engine ECU] Speed=%d RPM=%d\n",
            speed,
            rpm
        );

        sleep(1);
    }

    close(socket_fd);

    return 0;
}