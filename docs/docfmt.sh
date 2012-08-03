#!/bin/sh

rst2html --link-stylesheet docs.rst | 
sed '1,/<body>/d
/<\/body>/,$d' > docs.src

(cd ..; gitchangelog > CHANGES.txt)

rst2html --link-stylesheet ../CHANGES.txt | 
sed '1,/<body>/d
/<\/body>/,$d' > changelog.src

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
