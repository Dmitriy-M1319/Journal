configuration=$1
packet=''

case $configuration in
    'dev')
        packet='settings.dev_settings'
        ;;
    'prod')
        packet='settings.prod_settings'
        ;;
    *)
        echo 'Non valid configuration'
        ;;
esac
DJANGO_SETTINGS_MODULE=$packet ./manage.py runserver
