# pylog

Little Python logger module that prints stuff in a way I find helpful.

For usage see example.py .

When run it prints output like this:
```
2017-11-19 21:40:05.252949Z   debug   /0  double good habitat evaluator 2.0
2017-11-19 21:40:05.253023Z   info    /0/test_planet  {
2017-11-19 21:40:05.253055Z   verbose /0/test_planet  probe initialization
2017-11-19 21:40:05.253092Z   info    /0/test_planet/measuring  {
2017-11-19 21:40:05.253121Z   info    /0/test_planet/measuring  stickyness okay
2017-11-19 21:40:05.253149Z ! notice  /0/test_planet/measuring  foggy ground
2017-11-19 21:40:05.253184Z   info    /0/test_planet/measuring  } 0:00:00.000091
2017-11-19 21:40:05.253219Z ! warning /0/test_planet  exact measurements not possible
2017-11-19 21:40:05.253251Z   info    /0/test_planet  } 0:00:00.000231
2017-11-19 21:40:05.253285Z ! error   /0  habitat not suitable
```

