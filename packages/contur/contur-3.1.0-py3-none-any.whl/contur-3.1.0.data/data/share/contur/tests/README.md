To run the python tests, do `make check` in the top contur directory.

How to update the reference data
================================

If the regression tests are failing because of a valid change in Contur which means
the reference data need updating, here's how to do that.

First run `make check-keep`. This will build a test directory under $CONTUR_USER_DIR and will not delete it once the tests are done. 

The commands below assume you are in your local contur repository top directory.

In the `$CONTUR_USER_DIR/tests` you'll see the files `contur_run.db`, `contur.csv`, `yodastream_results.pkl` and `Summary.txt`. Copy these to your `test/sources` directory in your contur area. Rename `Summary.txt` to `single_yoda_run.txt` and `yodastream_results.pkl` to `yodastream_results_dict.pkl`.

```
cp $CONTUR_USER_DIR/tests/contur_run.db tests/sources/;
cp $CONTUR_USER_DIR/tests/contur.csv tests/sources/;
cp $CONTUR_USER_DIR/tests/single_results.db tests/sources/;
cp $CONTUR_USER_DIR/tests/spey_calc.csv tests/sources/;
cp $CONTUR_USER_DIR/tests/spey_results.db tests/sources/;
cp $CONTUR_USER_DIR/tests/yodastream_results.pkl tests/sources/yodastream_results_dict.pkl

```

The run `make check` to make sure everything passes, and commit and push the modified files.


If Rivet changed!
=================

If you need to regenerate the rivet data from which the regression test references are built (e.g. because new rivet routines have been added to Contur, or because bugs have been fixed in some Rivet routines) then you should do the following:

- copy $CONTUR_DATA_PATH/tests/sources/param_file.dat and $CONTUR_DATA_PATH/tests/sources/herwig.in into a local working directory

- make a RunInfo subdirectory and copy $CONTUR_DATA_PATH/data/Models/TopColour/SMWZP_UFO into it. run ufo2herwig and make as usual.

- then `contur-batch -b 7TeV,8TeV,13TeV -Q medium`

- Wait for the jobs to finish

- Run `contur -g myscan00 -s --whw --wbv --awz` on the resulting myscan00 directory.

- remove all the unnecessary files: `rm myscan00/*/*/herwig*.yoda.gz myscan00/*/*/herwig*.tex myscan00/*/*/runpoint_*.sh.e* myscan00/*/*/runpoint_*.sh.o*`

- move the old `test/sources/myscan00` to one side and copy your new one over in its place.

- update the regression references as described above.

