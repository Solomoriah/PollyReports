#!/bin/sh

rst2html --link-stylesheet docs.rst | 
sed '1,/<body>/d
/<\/body>/,$d' > docs.src

echo "Formatting..."

for i in *.src
do
    n=`basename "$i" .src`
    echo "$n.html"
    cat template.txt "$i" > "$n.html"
done

rm ../../pollyreports-pypi.zip
zip ../../pollyreports-pypi.zip *

# end of file.
