# Pysk - Python Server Konfigurator
by Philipp Wollermann

## History
Pysk was developed over the course of five years (2006 -  2011) by me, because I needed a software to manage my server infrastructure for my web hosting business. It was meant to be open-sourced quickly, but lots of hardcoded customer data and passwords, licensing issues, ugly source, lack of time, … kept me from actually publishing it. Finally, in 2012, I converted the trusty old hg repository to Git, rewrote history to remove the customer data and third-party components. Now there are only two "issues" left:

- Ugly source: We'll fix that someday and anyway, it's not as bad, as I remembered it to be.
- Passwords: They're still scattered through the history of some files, but don't worry about it. All the infrastructure from those days was shut down over a year ago, and all data deleted, so they can't be used anywhere. I could easily remove those parts, but then I'd have to change the history of the repository even more and you couldn't learn from looking at how the scripts really worked together and were developed.

## Current state
I didn't touch anything for over a year, but it was once a fully working system in daily use, managing over 40 virtual servers. There was a branch in which I heavily refactored everything, but it was non-functional at that time and was unfortunately lost. If you dig around, you'll find lots of interesting stuff, which is partly documented below - feel free to build your own management software using parts of Pysk. (Though you should probably have a look at Puppet or Chef before reinventing the wheel once again.)

## Architecture
- doc: Contains some personal notes for upgrading between versions, etc.
- etc/serverconfig: Contains configuration switches for invidivual servers
- - default: Default configuration switches
- - <hostname>: Create a file with the name of the server whose switches you want to override (see mikuru.igowo.de)
- etc/serverconfig/exclude:
- - <hostname>: Create a file with the name of the server, then list files which shouldn't be overwritten by the configuration management run (see kyon.igowo.de)
