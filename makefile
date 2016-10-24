FILES :=        \
    .gitignore  \
    .travis.yml \
    makefile    \
    apiary.apib \
    IDB1.log    \
    models.html \
    app/models.py   \
    app/tests.py    \
	UML.pdf

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
	echo "success";


clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

test:
	python3 app/tests.py

log:
	git log > IDB1.log
	# git log > IDB2.log
	# git log > IDB3.log

models.html: app/models.py
	cp app/models.py ./
	pydoc3 -w models
	rm models.py

artists: Scrape.py
	python3.5 -c 'import Scrape; Scrape.getids()'

albums: Scrape.py artist_ids_cache.pickle
	python3.5 -c 'import Scrape; Scrape.artist_album_list()'