# Python I2C Driver for Sensirion SFM3304

This repository contains the Python driver to communicate with a Sensirion SFM3304 sensor over I2C.

<img src="https://raw.githubusercontent.com/Sensirion/python-i2c-sfm3304/master/images/SFM3304.png"
    width="300px" alt="SFM3304 picture">


Click [here](https://sensirion.com/products/catalog/SFM3304-D) to learn more about the Sensirion SFM3304 sensor.



The default I²C address of [SFM3304](https://sensirion.com/products/catalog/SFM3304-D) is **0x2E**.



## Connect the sensor

You can connect your sensor over a [SEK-SensorBridge](https://developer.sensirion.com/sensirion-products/sek-sensorbridge/).
For special setups you find the sensor pinout in the section below.

<details><summary>Sensor pinout</summary>
<p>
<img src="https://raw.githubusercontent.com/Sensirion/python-i2c-sfm3304/master/images/Pinout-SFM3304.png"
     width="300px" alt="sensor wiring picture">

| *Pin* | *Cable Color* | *Name* | *Description*  | *Comments* |
|-------|---------------|:------:|----------------|------------|
| 1 |  | NC | Do not connect | Ground for the heater
| 2 | red | VDD | Supply Voltage | 3.15V to 3.45V
| 3 | yellow | SCL | I2C: Serial clock input |
| 4 | black | GND | Ground |
| 5 | green | SDA | I2C: Serial data input / output |
| 6 |  | NC | Do not connect | Supply voltage to the heater


</p>
</details>


## Documentation & Quickstart

See the [documentation page](https://sensirion.github.io/python-i2c-sfm3304) for an API description and a
[quickstart](https://sensirion.github.io/python-i2c-sfm3304/execute-measurements.html) example.


## Contributing

### Check coding style

The coding style can be checked with [`flake8`](http://flake8.pycqa.org/):

```bash
pip install -e .[test]  # Install requirements
flake8                  # Run style check
```

In addition, we check the formatting of files with
[`editorconfig-checker`](https://editorconfig-checker.github.io/):

```bash
pip install editorconfig-checker==2.0.3   # Install requirements
editorconfig-checker                      # Run check
```

## License

See [LICENSE](LICENSE).