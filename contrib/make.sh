#! /bin/sh -x
test "x${1+set}" = xset || set help

for i; do
    case "$i" in
	check)
	    flake8 account/ | grep -v /migrations
	    flake8 main/ | grep -v /migrations
	    ;;
	clean)
	    find . -type f -name '*~' -print | xargs rm -f
	    ;;
	distclean)
	    $0 clean
	    rm -f db.sqlite3 
	    find . -type d -name __pycache__ -print | xargs rm -rf
	    # find . -type f -empty -name __init__.py -print | xargs rm -f
	    rm -f */migrations/0*.py
	    ;;
	migrate)
	    python manage.py makemigrations --no-color 
	    python manage.py migrate --no-color
	    ;;
	test)
	    python manage.py test account main
	    ;;
	generate_secretkey)
	    python manage.py generate_secretkey --no-color 
	    ;;
	set_superuser)
	    echo 'Usage; python manage.py set_superuser --uid UID'
	    ;;
	dumptofile)
	    F="dumpdata_$(date '+%F_%T').json"
	    python manage.py dumpdata \
		   --exclude auth.permission --exclude contenttypes >${F}
	    gzip -v9 "${F}"
	    ;;
	showdump)
	    python manage.py dumpdata --indent 2 \
		   --exclude auth.permission --exclude contenttypes
	    ;;
	*)
	    echo "Usage: $0 [check|clean|distclean|migrate|generate_secretkey|set_superuser|dumptofile|showdump|help]"
	    ;;
    esac
done
