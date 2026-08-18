
Use this compile command to build the library and resolve the path issue for the lrose libs ...
```
jovyan@jupyter-projectpythia-erad2026-0geo0wno:~/notebooks/interop$ g++ -fPIC -shared -I/usr/local/lrose/include RadxEvad.cc -o liblroselite.so -L/usr/local/lrose/lib -ltoolsa -lphysics -lrapmath -ltdrp -lbz2 -lz -ldataport -Wl,-rpath,/usr/local/lrose/lib
```


