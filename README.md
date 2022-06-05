# BME280 dashboard


Simple web application that enables reading temperature, humidity and pressure measurements using dedicated BME280 sensor driver. Data is presented on a real-time charts as shown below.

![dashboard2](https://user-images.githubusercontent.com/39033831/172064782-c4b75a07-db02-4295-a7af-9c521593036f.png)

Proper functioning is only possible when the bme280 module is loaded to a kernel. Driver code is available in the [BME280_driver](https://github.com/tuuznik/BME280_driver) repository. Both driver and the application need to be running on a device to which BME280 sensor is connected. The project was developed on Raspberry Pi 4B and it is advised to run it in the same environment.

If everything is setup correctly, *start* button starts measurements. By default these are read every second, however it can be modified in the code. At this point, there is no such option directly from the dashboard. *Stop* button stops measurements. It is possible to download all saved data in csv format or clear saved measurements by using corresponding buttons.
