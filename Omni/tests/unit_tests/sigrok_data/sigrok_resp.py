
version_rsp = """sigrok-cli 0.7.2

Libraries and features:
- libsigrok 0.5.2/5:1:1 (rt: 0.5.2/5:1:1).
 - Libs:
  - glib 2.67.5 (rt: 2.72.4/7204:4)
  - libzip 1.7.3
  - libserialport 0.1.1/1:0:1 (rt: 0.1.1/1:0:1)
  - libusb-1.0 1.0.25.11696 API 0x01000108
  - hidapi 0.10.1
  - bluez 5.56
  - libftdi 1.5
  - Host: x86_64-pc-linux-gnu, little-endian.
  - SCPI backends: TCP, serial, USBTMC.
- libsigrokdecode 0.5.3/6:1:2 (rt: 0.5.3/6:1:2).
 - Libs:
  - glib 2.71.1 (rt: 2.72.4/7204:4)
  - Python 3.10.2 / 0x30a02f0 (API 1013, ABI 3)
  - Host: x86_64-pc-linux-gnu, little-endian."""

help_rsp = '''Usage:
  sigrok-cli [OPTION?]

Help Options:
  -h, --help                             Show help options

Application Options:
  -V, --version                          Show version
  -L, --list-supported                   List supported devices/modules/decoders
  --list-supported-wiki                  List supported decoders (MediaWiki)
  -l, --loglevel                         Set loglevel (5 is most verbose)
  -d, --driver                           The driver to use
  -c, --config                           Specify device configuration options
  -i, --input-file                       Load input from file
  -I, --input-format                     Input format
  -o, --output-file                      Save output to file
  -O, --output-format                    Output format
  -T, --transform-module                 Transform module
  -C, --channels                         Channels to use
  -g, --channel-group                    Channel groups
  -t, --triggers                         Trigger configuration
  -w, --wait-trigger                     Wait for trigger
  -P, --protocol-decoders                Protocol decoders to run
  -A, --protocol-decoder-annotations     Protocol decoder annotation(s) to show
  -M, --protocol-decoder-meta            Protocol decoder meta output to show
  -B, --protocol-decoder-binary          Protocol decoder binary output to show
  --protocol-decoder-ann-class           Show annotation class in decoder output
  --protocol-decoder-samplenum           Show sample numbers in decoder output
  --protocol-decoder-jsontrace           Output in Google Trace Event format (JSON)
  --scan                                 Scan for devices
  -D, --dont-scan                        Don't auto-scan (use -d spec only)
  --show                                 Show device/format/decoder details
  --time                                 How long to sample (ms)
  --samples                              Number of samples to acquire
  --frames                               Number of frames to acquire
  --continuous                           Sample continuously
  --get                                  Get device options only
  --set                                  Set device options only
  --list-serial                          List available serial/HID/BT/BLE ports'''
