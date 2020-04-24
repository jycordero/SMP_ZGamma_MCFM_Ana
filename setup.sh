#bin/bash!

export PYTHONWORKDIR=/home/jcordero/CMS/SMP_ZGamma_MCFM_Ana/python
export PYTHONPATH=$PYTHONPATH:/home/jcordero/CMS/SMP_ZGamma_MCFM_Ana/python

TOPDIR=$PWD
SUBDIRS=( ../src Plotter Reader )
for DIR in ${SUBDIRS[@]} 
do
	jupyter nbconvert --to script *.ipynb
	cd $PYTHONWORKDIR/$DIR/jupyter
	echo "In " $PWD
	echo "Performing : jupyter nbconvert --to script $PYTHONWORKDIR/$DIR/*.ipynb"
	jupyter nbconvert --to script *.ipynb
	mv *.py $PYTHONWORKDIR/$DIR

	cd $TOPDIR
	printf "\n\n"
done

