{ pkgs
, buildPythonPackage
, fetchurl
, extras ? []
, ...
}:

with pkgs;
with pythonPackages;

rec {

  babel = buildPythonPackage {
      name = "babel-2.4.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/5f/cf/17935db603f7044d188ce3e3a6545c4b4500dbaa8835d50da2934b738111/Babel-2.4.0-py2.py3-none-any.whl";
        sha256 = "e86ca5a3a6bb64b9bbb62b9dac37225ec0ab5dfaae3c2492ebd648266468042f";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ pytz ];
      doCheck = false;
    }
    ;
  cliff = buildPythonPackage {
      name = "cliff-2.5.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/ad/6a/fa13606e6ef44b9ef0b152e78bad9c2b829c7ca3a4165c61dd6bb18b978e/cliff-2.5.0-py2-none-any.whl";
        sha256 = "69be930f40402582a1807d76790cb2e578af7dc70651e0f9fcc600088ecbf99a";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ cmd2 pbr prettytable pyyaml stevedore unicodecsv ];
      doCheck = false;
    }
    ;
  cmd2 = buildPythonPackage {
      name = "cmd2-0.7.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/9b/58/e88fda298b521e6073d4dd7f305cf661d805d1c06fd86f44ccc2f271a800/cmd2-0.7.0.tar.gz";
        sha256 = "5ab76a1f07dd5fd1cc3c15ba4080265f33b80c7fd748d71bd69a51d60b30f51a";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  debtcollector = buildPythonPackage {
      name = "debtcollector-1.13.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/9a/20/8e8819a267849c5578b84ad073c2e2daf48b0260ced4be8a7755e10ae0b0/debtcollector-1.13.0-py2.py3-none-any.whl";
        sha256 = "a2dc44307da6f17432c63eb947b3bce0c43a9b3f4291fd62e9e6a3969f3c6645";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ funcsigs pbr wrapt ];
      doCheck = false;
    }
    ;
  decorator = buildPythonPackage {
      name = "decorator-4.0.11";
      src = fetchurl {
        url = "https://pypi.python.org/packages/cc/ac/5a16f1fc0506ff72fcc8fd4e858e3a1c231f224ab79bb7c4c9b2094cc570/decorator-4.0.11.tar.gz";
        sha256 = "953d6bf082b100f43229cf547f4f97f97e970f5ad645ee7601d55ff87afdfe76";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  deprecation = buildPythonPackage {
      name = "deprecation-1.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/ab/fe/edad444ecab087e57dd32a10e38ef0d7448b3ab8ff8bfa65b022d3a43a1c/deprecation-1.0.tar.gz";
        sha256 = "36d2a2356ca89fb73f72bfb866a2f28e183535a7f131a3b34036bc48590165b6";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  dogpile-cache = buildPythonPackage {
      name = "dogpile.cache-0.6.2";
      src = fetchurl {
        url = "https://pypi.python.org/packages/9d/a9/ba70aadc6170841a1c6145e9039d4b1c2a4ef8c44cd0ca9b09ab79be9120/dogpile.cache-0.6.2.tar.gz";
        sha256 = "73793471af07af6dc5b3ee015abfaca4220caaa34c615537f5ab007ed150726d";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  funcsigs = buildPythonPackage {
      name = "funcsigs-1.0.2";
      src = fetchurl {
        url = "https://pypi.python.org/packages/94/4a/db842e7a0545de1cdb0439bb80e6e42dfe82aaeaadd4072f2263a4fbed23/funcsigs-1.0.2.tar.gz";
        sha256 = "a7bb0f2cf3a3fd1ab2732cb49eba4252c2af4240442415b4abce3b87022a8f50";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  functools32 = buildPythonPackage {
      name = "functools32-3.2.3-2";
      src = fetchurl {
        url = "https://pypi.python.org/packages/c5/60/6ac26ad05857c601308d8fb9e87fa36d0ebf889423f47c3502ef034365db/functools32-3.2.3-2.tar.gz";
        sha256 = "f6253dfbe0538ad2e387bd8fdfd9293c925d63553f5813c4e587745416501e6d";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  futures = buildPythonPackage {
      name = "futures-3.0.5";
      src = fetchurl {
        url = "https://pypi.python.org/packages/9c/3f/1d818ea03fb2956a2bdfa8f8a3b1319590f0f151a5584a8a3ae45085066c/futures-3.0.5-py2-none-any.whl";
        sha256 = "f7f16b6bf9653a918a03f1f2c2d62aac0cd64b1bc088e93ea279517f6b61120b";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  ipaddress = buildPythonPackage {
      name = "ipaddress-1.0.18";
      src = fetchurl {
        url = "https://pypi.python.org/packages/4e/13/774faf38b445d0b3a844b65747175b2e0500164b7c28d78e34987a5bfe06/ipaddress-1.0.18.tar.gz";
        sha256 = "5d8534c8e185f2d8a1fda1ef73f2c8f4b23264e8e30063feeb9511d492a413e1";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  iso8601 = buildPythonPackage {
      name = "iso8601-0.1.11";
      src = fetchurl {
        url = "https://pypi.python.org/packages/c0/75/c9209ee4d1b5975eb8c2cba4428bde6b61bd55664a98290dd015cdb18e98/iso8601-0.1.11.tar.gz";
        sha256 = "e8fb52f78880ae063336c94eb5b87b181e6a0cc33a6c008511bac9a6e980ef30";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  jmespath = buildPythonPackage {
      name = "jmespath-0.9.2";
      src = fetchurl {
        url = "https://pypi.python.org/packages/10/3b/968949a364f7f9fb9ff5acec3b98df2d74c201ab5f0cd07fa6c48ea227c2/jmespath-0.9.2-py2.py3-none-any.whl";
        sha256 = "3f03b90ac8e0f3ba472e8ebff083e460c89501d8d41979771535efe9a343177e";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  jsonpatch = buildPythonPackage {
      name = "jsonpatch-1.15";
      src = fetchurl {
        url = "https://pypi.python.org/packages/be/c1/947048a839120acefc13a614280be3289db404901d1a2d49b6310c6d5757/jsonpatch-1.15.tar.gz";
        sha256 = "ae23cd08b2f7246f8f2475363501e740c4ef93f08f2a3b7b9bcfac0cc37fceb1";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [ jsonpointer ];
      doCheck = false;
    }
    ;
  jsonpointer = buildPythonPackage {
      name = "jsonpointer-1.10";
      src = fetchurl {
        url = "https://pypi.python.org/packages/f6/36/6bdd302303e8bc7c25102dbc1eabb3e3d97f57b0f8f414f4da7ea7ab9dd8/jsonpointer-1.10.tar.gz";
        sha256 = "9fa5dcac35eefd53e25d6cd4c310d963c9f0b897641772cd6e5e7b89df7ee0b1";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  jsonschema = buildPythonPackage {
      name = "jsonschema-2.6.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/58/b9/171dbb07e18c6346090a37f03c7e74410a1a56123f847efed59af260a298/jsonschema-2.6.0.tar.gz";
        sha256 = "6ff5f3180870836cae40f06fa10419f557208175f13ad7bc26caa77beb1f6e02";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [ functools32 ];
      doCheck = false;
    }
    ;
  keystoneauth1 = buildPythonPackage {
      name = "keystoneauth1-2.19.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/ad/41/29e8c0c943756b9a2ee704f0a6bcf176c8fc11a93a73f1c62c38f3e1d385/keystoneauth1-2.19.0-py2.py3-none-any.whl";
        sha256 = "65f326456bcb0bb6bde03a23bb29f85fdb2df10a3e6b65f88a6536829983175d";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ iso8601 pbr positional requests stevedore wrapt ];
      doCheck = false;
    }
    ;
  monotonic = buildPythonPackage {
      name = "monotonic-1.3";
      src = fetchurl {
        url = "https://pypi.python.org/packages/96/b3/3e9fa0bdf132a971571cbf0e3f0c8b38834f4f7af8ca9523794f4f5895e0/monotonic-1.3.tar.gz";
        sha256 = "2b469e2d7dd403f7f7f79227fe5ad551ee1e76f8bb300ae935209884b93c7c1b";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  msgpack-python = buildPythonPackage {
      name = "msgpack-python-0.4.8";
      src = fetchurl {
        url = "https://pypi.python.org/packages/21/27/8a1d82041c7a2a51fcc73675875a5f9ea06c2663e02fcfeb708be1d081a0/msgpack-python-0.4.8.tar.gz";
        sha256 = "1a2b19df0f03519ec7f19f826afb935b202d8979b0856c6fb3dc28955799f886";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  munch = buildPythonPackage {
      name = "munch-2.1.1";
      src = fetchurl {
        url = "https://pypi.python.org/packages/84/dc/d897cb427f15029e04745a3de611d8ed3d97e9a0ef894547a0ba261f2807/munch-2.1.1.tar.gz";
        sha256 = "648b650d1eb0173bd83c29f2eea2568b7591c1e05c87971387d170c71c6397e8";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  netaddr = buildPythonPackage {
      name = "netaddr-0.7.19";
      src = fetchurl {
        url = "https://pypi.python.org/packages/0c/13/7cbb180b52201c07c796243eeff4c256b053656da5cfe3916c3f5b57b3a0/netaddr-0.7.19.tar.gz";
        sha256 = "38aeec7cdd035081d3a4c306394b19d677623bf76fa0913f6695127c7753aefd";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  netifaces = buildPythonPackage {
      name = "netifaces-0.10.5";
      src = fetchurl {
        url = "https://pypi.python.org/packages/a7/4c/8e0771a59fd6e55aac993a7cc1b6a0db993f299514c464ae6a1ecf83b31d/netifaces-0.10.5.tar.gz";
        sha256 = "59d8ad52dd3116fcb6635e175751b250dc783fb011adba539558bd764e5d628b";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  openstacksdk = buildPythonPackage {
      name = "openstacksdk-0.9.14";
      src = fetchurl {
        url = "https://pypi.python.org/packages/a8/02/c999d8932cfdc4ea953260d909587e94483e21c6b298b5c9f6d7e97b0c29/openstacksdk-0.9.14-py2.py3-none-any.whl";
        sha256 = "7d1a1fcf5586c6b16b409270d5b861d0969ac0a14a1a5ddfdf95df5be5daab89";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ deprecation iso8601 keystoneauth1 os-client-config pbr positional pyyaml requests requestsexceptions stevedore wrapt ];
      doCheck = false;
    }
    ;
  os-client-config = buildPythonPackage {
      name = "os-client-config-1.26.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/f4/de/5feba3da1a4b65053418e7ad738ccc76a6da5e0a484e8647905ee5cd93c5/os_client_config-1.26.0-py2.py3-none-any.whl";
        sha256 = "f9a14755f9e498eb5eef553b8b502a08a033fe3993c7152ce077696b1d37c4f4";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ keystoneauth1 pyyaml requestsexceptions ];
      doCheck = false;
    }
    ;
  osc-lib = buildPythonPackage {
      name = "osc-lib-1.3.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/47/8b/3c1ef95bcac763a4f3caa2348b641422b6283c89eb4736eeeebdbbffa28a/osc_lib-1.3.0-py2-none-any.whl";
        sha256 = "4817d2d7e3332809d822046297650fec70eceff628be419046ebd66577d16b03";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ babel cliff cmd2 debtcollector funcsigs iso8601 keystoneauth1 monotonic netaddr netifaces os-client-config oslo-i18n oslo-utils pbr positional prettytable pytz pyyaml requests requestsexceptions simplejson stevedore unicodecsv wrapt ];
      doCheck = false;
    }
    ;
  oslo-config = buildPythonPackage {
      name = "oslo.config-3.24.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/5f/3d/eb1ae473c55509ec1c0b1d6e40a97b5fc862f747615cedad91fcb9b2006c/oslo.config-3.24.0-py2.py3-none-any.whl";
        sha256 = "d79ece78ff3ff5dd075b50c2e69e4359a86546f9e9333bafe5220929549d5f5c";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ babel debtcollector funcsigs netaddr oslo-i18n pbr pytz rfc3986 stevedore wrapt ];
      doCheck = false;
    }
    ;
  oslo-i18n = buildPythonPackage {
      name = "oslo.i18n-3.15.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/01/73/5cf947a5dd5dbca0f264f6bf0b7cd9b025699167826526ffc815b8466e5a/oslo.i18n-3.15.0-py2.py3-none-any.whl";
        sha256 = "4d01410167af8b874f44af8515218c3b18171be9796abc9f3d0cf4257b4cbcd4";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ babel pbr ];
      doCheck = false;
    }
    ;
  oslo-serialization = buildPythonPackage {
      name = "oslo.serialization-2.18.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/ed/ed/594b660cc7f07bbcf91ebdbfdda0be2dc31a42a873ae004bea22612351eb/oslo.serialization-2.18.0-py2.py3-none-any.whl";
        sha256 = "1fe5fba373f338402e14266c91d092a73297753ce306d3f1905c1079891fac33";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ babel debtcollector funcsigs iso8601 monotonic msgpack-python netaddr netifaces oslo-i18n oslo-utils pbr pytz wrapt ];
      doCheck = false;
    }
    ;
  oslo-utils = buildPythonPackage {
      name = "oslo.utils-3.25.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/a6/32/f83357ed7832e28f55027786e0175475888d82299ac4010adb0e71603fc7/oslo.utils-3.25.0-py2.py3-none-any.whl";
        sha256 = "714ee981dfd81c94f9bc16e54788a34d9f427152b082811d118e78b19a9d00c1";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ debtcollector iso8601 monotonic netaddr netifaces oslo-i18n ];
      doCheck = false;
    }
    ;
  pbr = buildPythonPackage {
      name = "pbr-2.0.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/e9/c0/8f7f54d7b9b8ceb73ac30d769fdd722431e95ad0d2cd689def382e8b9eec/pbr-2.0.0-py2.py3-none-any.whl";
        sha256 = "d9b69a26a5cb4e3898eb3c5cea54d2ab3332382167f04e30db5e1f54e1945e45";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  positional = buildPythonPackage {
      name = "positional-1.1.1";
      src = fetchurl {
        url = "https://pypi.python.org/packages/83/73/1e2c630d868b73ecdea381ad7b081bc53888c07f1f9829699d277a2859a8/positional-1.1.1.tar.gz";
        sha256 = "ef845fa46ee5a11564750aaa09dd7db059aaf39c44c901b37181e5ffa67034b0";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [ pbr wrapt ];
      doCheck = false;
    }
    ;
  prettytable = buildPythonPackage {
      name = "prettytable-0.7.2";
      src = fetchurl {
        url = "https://pypi.python.org/packages/ef/30/4b0746848746ed5941f052479e7c23d2b56d174b82f4fd34a25e389831f5/prettytable-0.7.2.tar.bz2";
        sha256 = "853c116513625c738dc3ce1aee148b5b5757a86727e67eff6502c7ca59d43c36";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  python-cinderclient = buildPythonPackage {
      name = "python-cinderclient-2.0.1";
      src = fetchurl {
        url = "https://pypi.python.org/packages/83/2f/aefb6215b7576969c4fca15f35dc3d931a8c22520b0c786e27074de834b5/python_cinderclient-2.0.1-py2.py3-none-any.whl";
        sha256 = "aa6c3614514d28bd13006a2220a559f10088ceb54b7506888131f95942c158bc";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ babel debtcollector funcsigs iso8601 keystoneauth1 monotonic netaddr netifaces oslo-i18n oslo-utils pbr positional prettytable pytz requests simplejson stevedore wrapt ];
      doCheck = false;
    }
    ;
  python-designateclient = buildPythonPackage {
      name = "python-designateclient-2.6.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/f8/15/4ac00b87d121e3bc44bc04b6025e0014c8e38ac7f65e693db0e18de2d15c/python_designateclient-2.6.0-py2.py3-none-any.whl";
        sha256 = "cfc980c1f7c77ad87113b3d67b04aa08adedd94b8d456aed29df3358e9be048e";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ babel cliff cmd2 debtcollector funcsigs functools32 iso8601 jsonschema keystoneauth1 monotonic netaddr netifaces os-client-config osc-lib oslo-i18n oslo-utils pbr positional prettytable pytz pyyaml requests requestsexceptions simplejson stevedore unicodecsv wrapt ];
      doCheck = false;
    }
    ;
  python-glanceclient = buildPythonPackage {
      name = "python-glanceclient-2.6.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/6e/c1/b9d59ad77dba5d7f036d23b7aadea89447305aa145aaaa5cf1f76a849c38/python_glanceclient-2.6.0-py2.py3-none-any.whl";
        sha256 = "e77e63de240f4e183a0960c83eb434774746156571c9ea7e7ef4421365b1a762";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ babel debtcollector funcsigs functools32 iso8601 jsonpatch jsonpointer jsonschema keystoneauth1 monotonic netaddr netifaces oslo-i18n oslo-utils pbr positional prettytable pytz requests stevedore warlock wrapt ];
      doCheck = false;
    }
    ;
  python-ironicclient = buildPythonPackage {
      name = "python-ironicclient-1.12.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/07/50/984bd21bc296fc53231abc2860ca5d54a3b4e6c8ceddb4da4e436466d86a/python_ironicclient-1.12.0-py2.py3-none-any.whl";
        sha256 = "d6c6ad52bdd38fe3ad9403a6129038f862bdfe0dc4e0eca143351d340df092cf";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ babel cliff cmd2 debtcollector deprecation dogpile-cache funcsigs functools32 iso8601 jsonpatch jsonpointer jsonschema keystoneauth1 monotonic msgpack-python netaddr netifaces openstacksdk os-client-config osc-lib oslo-config oslo-i18n oslo-serialization oslo-utils pbr positional prettytable python-cinderclient python-glanceclient python-keystoneclient python-novaclient python-openstackclient pytz pyyaml requests requestsexceptions rfc3986 simplejson stevedore unicodecsv warlock wrapt ];
      doCheck = false;
    }
    ;
  python-keystoneclient = buildPythonPackage {
      name = "python-keystoneclient-3.10.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/ee/a9/c51a1657f655171d599b43be31b6df5b6d47d83e91595ca43de7bee950cd/python_keystoneclient-3.10.0-py2.py3-none-any.whl";
        sha256 = "f30dd06d03f1f85af0cfa18c270e23d2ffd9e776c11c1b534f6ea503e4f31d80";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ keystoneauth1 oslo-config oslo-serialization ];
      doCheck = false;
    }
    ;
  python-neutronclient = buildPythonPackage {
      name = "python-neutronclient-6.1.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/6d/bf/aa1ebe9de4a92648afe29e692c07d410fde6e1fc914f3dfa3773f39208f5/python_neutronclient-6.1.0-py2.py3-none-any.whl";
        sha256 = "55f9e9b5cba27f6d9bc2b1b4d894764cb94e42054ebf5a1d701b1bf5ac5ecb4a";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ babel cliff cmd2 debtcollector funcsigs iso8601 keystoneauth1 monotonic msgpack-python netaddr netifaces os-client-config osc-lib oslo-config oslo-i18n oslo-serialization oslo-utils pbr positional prettytable python-keystoneclient pytz pyyaml requests requestsexceptions rfc3986 simplejson stevedore unicodecsv wrapt ];
      doCheck = false;
    }
    ;
  python-novaclient = buildPythonPackage {
      name = "python-novaclient-8.0.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/f2/6e/c000650710f52aa8cc3b5a7904b398aed8b41f220cda0a2f48c481beb9cb/python_novaclient-8.0.0-py2.py3-none-any.whl";
        sha256 = "a428f5acc19bd41bcb7401bd9fadfcbcdeb8786620958e02f038bd49e05c0e69";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ keystoneauth1 oslo-serialization prettytable simplejson ];
      doCheck = false;
    }
    ;
  python-openstackclient = buildPythonPackage {
      name = "python-openstackclient-3.9.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/f7/02/cc20ac2b50af74781186fcf8b0599acbfb21238122c830a0cfce936526ef/python_openstackclient-3.9.0-py2.py3-none-any.whl";
        sha256 = "3c48e9bbdff8a7679f04fe6a03d609c75e597975f9f43de7ec001719ec554ad9";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ openstacksdk osc-lib python-cinderclient python-glanceclient python-keystoneclient python-novaclient ];
      doCheck = false;
    }
    ;
  pytz = buildPythonPackage {
      name = "pytz-2017.2";
      src = fetchurl {
        url = "https://pypi.python.org/packages/55/62/e7cd0e15b76062d298413f14bb4ec3cd8568a22d274427f9c3c7286969f4/pytz-2017.2-py2.py3-none-any.whl";
        sha256 = "d1d6729c85acea5423671382868627129432fba9a89ecbb248d8d1c7a9f01c67";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  pyyaml = buildPythonPackage {
      name = "pyyaml-3.12";
      src = fetchurl {
        url = "https://pypi.python.org/packages/4a/85/db5a2df477072b2902b0eb892feb37d88ac635d36245a72a6a69b23b383a/PyYAML-3.12.tar.gz";
        sha256 = "592766c6303207a20efc445587778322d7f73b161bd994f227adaa341ba212ab";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  requests = buildPythonPackage {
      name = "requests-2.12.5";
      src = fetchurl {
        url = "https://pypi.python.org/packages/bf/99/af6139323bac0ca0c6023eabbdc526579525f5584278d001dd2e169f8300/requests-2.12.5-py2.py3-none-any.whl";
        sha256 = "d57dae49f4267e8cb378aff9e426c9304a78794d03e945e39bfc607355715658";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  requestsexceptions = buildPythonPackage {
      name = "requestsexceptions-1.2.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/b6/ac/659483588ad847056ddf01062bca15995b95463efb859e9e2672847dca84/requestsexceptions-1.2.0-py2.py3-none-any.whl";
        sha256 = "f4b43338e69bb7038d2a4ad8cce6b9240e2d272aaf437bd18a2dc9eba25a735c";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ pbr ];
      doCheck = false;
    }
    ;
  rfc3986 = buildPythonPackage {
      name = "rfc3986-0.4.1";
      src = fetchurl {
        url = "https://pypi.python.org/packages/82/53/c3ee5a1869fdf5d1d02c344ed939769b886178ec7ba91d5200e1c779bc87/rfc3986-0.4.1-py2.py3-none-any.whl";
        sha256 = "6823e63264be3da1d42b3ec0e393dc8e6d03fd5e28d4291b797c76cf33759061";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  shade = buildPythonPackage {
      name = "shade-1.19.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/54/32/a53b07af77b4397a83fe861b4fd0fc4caea2a93cdba579419ea4428246a0/shade-1.19.0-py2-none-any.whl";
        sha256 = "eba474944eab686a5a32ba4ec7010941898c9cd17d3ea6220c5253392ede458b";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ decorator futures ipaddress jmespath munch python-designateclient python-ironicclient python-neutronclient ];
      doCheck = false;
    }
    ;
  simplejson = buildPythonPackage {
      name = "simplejson-3.10.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/40/ad/52c1f3a562df3b210e8f165e1aa243a178c454ead65476a39fa3ce1847b6/simplejson-3.10.0.tar.gz";
        sha256 = "953be622e88323c6f43fad61ffd05bebe73b9fd9863a46d68b052d2aa7d71ce2";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  stevedore = buildPythonPackage {
      name = "stevedore-1.21.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/3e/9b/79ad5d29da9453a81707ae0730543d3ea21061dd98afbf0b5d0eaa20a9b9/stevedore-1.21.0-py2.py3-none-any.whl";
        sha256 = "a015fb150871247e385153e98cc03c373a857157628b4746bfdf8501e82e9a3d";
      };
      format = "wheel";
      buildInputs = [  ];
      propagatedBuildInputs = [ pbr ];
      doCheck = false;
    }
    ;
  unicodecsv = buildPythonPackage {
      name = "unicodecsv-0.14.1";
      src = fetchurl {
        url = "https://pypi.python.org/packages/6f/a4/691ab63b17505a26096608cc309960b5a6bdf39e4ba1a793d5f9b1a53270/unicodecsv-0.14.1.tar.gz";
        sha256 = "018c08037d48649a0412063ff4eda26eaa81eff1546dbffa51fa5293276ff7fc";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  warlock = buildPythonPackage {
      name = "warlock-1.2.0";
      src = fetchurl {
        url = "https://pypi.python.org/packages/0f/d4/408b936a3d9214b7685c35936bb59d9254c70ff319ee6a837b9efcf5615e/warlock-1.2.0.tar.gz";
        sha256 = "7c0d17891e14cf77e13a598edecc9f4682a5bc8a219dc84c139c5ba02789ef5a";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [ jsonpatch jsonschema ];
      doCheck = false;
    }
    ;
  wrapt = buildPythonPackage {
      name = "wrapt-1.10.10";
      src = fetchurl {
        url = "https://pypi.python.org/packages/a3/bb/525e9de0a220060394f4aa34fdf6200853581803d92714ae41fc3556e7d7/wrapt-1.10.10.tar.gz";
        sha256 = "42160c91b77f1bc64a955890038e02f2f72986c01d462d53cb6cb039b995cdd9";
      };
      format = "setuptools";
      buildInputs = [  ];
      propagatedBuildInputs = [  ];
      doCheck = false;
    }
    ;
  

}