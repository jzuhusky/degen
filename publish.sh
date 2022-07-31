#!/bin/bash


read -p "Please confirm the version you're publishing " VERSION

echo $VERSION

if [ $VERSION = $(cat __version__.txt) ]; then
		echo "Version's match!"
		echo "."
		echo "."
		echo "."
else
		echo "Versions don't match!"
		exit 1;
fi;

echo "Packaging things up..."
echo "."
echo "."
echo "."
python setup.py sdist


echo "Publishing..."
echo "."
echo "."
echo "."
twine upload --repository pypi dist/degen-$VERSION.tar.gz

echo "All done!"
