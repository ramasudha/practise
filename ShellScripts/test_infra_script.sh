#!/bin/bash
############################################################################
#                                                                          #
#                   Test Infra Bringup Script                              #
#                                                                          #
############################################################################

prepare_a4_test_workspace () {
    echo "Bringing up a4 test infrastructure"
    sudo apt-get -qq update 2>/dev/null

    echo "Installing required python packages"
    sudo apt-get -qq install python-pip python3-pip sshpass -y  2>/dev/null
    sudo apt-get -qq install build-essential libssl-dev libffi-dev \
         python-dev -y  2>/dev/null

    req_packages="nose==1.3.7 \
             nose-html==1.1 \
             nose-htmloutput==0.6.0 \
             nose2-html-report==0.5.0 \
             html-testRunner==1.1.1 \
             pexpect==4.0.1 \
             requests==2.9.1 \
             responses==0.3.0 \
             coverage==4.4.2 \
             texttable \
             argparse
             progressbar2"
    for package in $req_packages; do
        echo "Installing $package"
        sudo -H pip3 -q install "$package"
    done
}

download_packages () {
    mkdir -p ~/TEST

    CUT_DIR_CNT=$(echo $REPO_IP | grep -c "/")
    let CUT_DIR_CNT+=1

    sshpass -p 'pod' scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -r pod@$REPO_IP:/var/www/html/dt_a4/ . 2>/dev/null
    wget -q -r -m -nH --cut-dirs=$CUT_DIR_CNT --no-parent --reject="index.html*" \
        http://$REPO_IP/dt_a4/test_harness/ -P ~/TEST

    cd ~/TEST && chmod -R +x *

    sudo mv /usr/local/lib/python3.5/dist-packages/nose_htmloutput/templates/report.html \
        /usr/local/lib/python3.5/dist-packages/nose_htmloutput/templates/report.html_bak
    sudo cp ~/TEST/test_harness/report_template.html \
        /usr/local/lib/python3.5/dist-packages/nose_htmloutput/templates/report.html

    sudo mkdir -p /var/www/html/dt_thf/

    sudo rm /var/www/html/a4_pod_config.json 2>/dev/null
    sudo rm /var/www/html/a4_service_config.json 2>/dev/null
    sudo rm /var/www/html/a4_service_deps.json 2>/dev/null

    sudo wget -q http://$REPO_IP/dt_a4/manifest/config/a4_pod_config.json -P /var/www/html/
    sudo wget -q http://$REPO_IP/dt_a4/manifest/config/a4_service_config.json -P /var/www/html/
    sudo wget -q http://$REPO_IP/dt_a4/manifest/config/a4_service_deps.json -P /var/www/html/


    echo "******************************************************************"
    echo ""
    echo "!!!  Infra for Automation and Test Harness framework is ready  !!!"
    echo ""
    echo "******************************************************************"
}

usage()
{
    echo "`basename ${0}`
usage:
      -r      repo_ip
      -h      Help
    "
    exit 1
}

if [ $# -lt 1 ]; then
    usage
fi

while getopts ":hr:" arg; do
    case $arg in
        r) echo ${OPTARG}
        REPO_IP=${OPTARG};;
        h|*) usage;;
    esac
done

prepare_a4_test_workspace
download_packages
