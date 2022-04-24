<div id="top"></div>

<!-- PROJECT SHIELDS -->

<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">ovpn4snom</h3>

  <p align="center">
    Ovpn4snom is a Python script to convert a OpenVPN configuration, in ovpn format, into a snom VoIP phone compatible tarball.
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

Instead of copy and paste certificates, key and OpenVPN configuration out of an ovpn file, this Python script ist doing all of this tasks for you and will provide a ready to use tarball you can use to transfer to your snom VoIP phone. The snom VoIP phone need to have OpenVPN featured firmware installed. 

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

* [Python3](https://www.python.org/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

* pip
  ```sh
   pip3 install paramiko
   pip3 install python-gnupg
  ```

### Installation


1. Clone the repo
   ```sh
   git clone https://github.com/skruszka/ovpn4snom.git
   ```
2. Install pip3 packages
   ```sh
   pip3 install argparse
   pip3 install getpass
   pip3 install tarfile
   ```
<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

```sh
usage: ovpn4snom.py [-h] [-A] [-p PASSWD] [-u USERNAME] [-f FILE] [-v]

Create openvpn configuration, certificates, key and tarball for snom VoIP phones with OpenVPN firmware

optional arguments:
  -h, --help            show this help message and exit
  -A, --auth            Create file for user credential for authentication
  -p PASSWD, --passwd PASSWD
                        Password of the authentication user
  -u USERNAME, --username USERNAME
                        Username of the authentication user
  -f FILE, --file FILE  Filename of the ovpn file, default file is client.ovpn
  -v, --verbose         Enables verbose output
```
For more information on how to use the generated tarball with your snom VoIP Phone, please visit https://service.snom.com/display/wiki/Configuring+VPN+on+Snom+Deskphones

<!-- ROADMAP -->
## Roadmap

These are not the features you are looking for!

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

## License

Distributed under the GNU General Public License v3.0. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Sascha Kruszka - sascha.kruszka@googlemail.com

<p align="right">(<a href="#top">back to top</a>)</p>
