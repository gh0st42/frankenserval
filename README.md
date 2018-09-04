# frankenserval
Frankenstein's Serval 
```

                                                   .....
                                                  C C  /
                                                 /<   /
                                  ___ __________/_#__=o
                                /(- /(\_\________   \
                                \ ) \ )_      \o     \
                                /|\ /|\       |'     |
                                              |     _|
                                              /o   __\
                                             / '     |
                                            / /      |
                                           /_/\______|
    _                ___       _.--.      (   _(    <
    \`.|\..----...-'`   `-._.-'_.-'`       \    \    \
    /  ' `         ,       __.--'           \    \    |
    )/' _/     \   `-_,   /                  \____\____\
    `-'" `"\_  ,_.-;_.-\_ ',     fsc/as    ____\_\__\_\
        _.-'_./   {_.'   ; /              /`   /`     o\
       {_.-``-'         {_/               |___ |_______|.. . b'ger
```



    

    


               

Proof-of-Concept of a MDP-less serval communicating only over HTTP similar to (forban)[https://github.com/adulau/Forban]. This is a hacky python version, current rhizome state is locally checked via restful every 2 seconds. HTTP direct sync is only triggered if two nodes announce different hashes. 

## Usage

Prevent serval from using MDP on any interface by removing them from the config:
```
$ servald config del interfaces.0.match
```

Make sure that pum:pum123 have restful access to serval instance on 127.0.0.1:
```
$ servald config set api.restful.users.pum.password pum123
```

Finally, execute `python frankenserval.py`

*NOTE: Default announcement interval 2s*