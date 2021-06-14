#!/usr/bin/env bash

ENV=''
PRJ_ROOT=$(cd $(dirname $0) && cd ../ && pwd)

usage_exit() {
    echo "Usage: docker-compose run --rm app yarn run deploy [-s env]"
    echo "-s dev: ステージング環境"
    echo "-s prod: 本番環境"
    exit 1
}

while getopts s:rh OPT
do
    case $OPT in
        \?) OPT_ERROR=1;
            break
            ;;
        s)  ENV=$OPTARG
            ;;
        h)  usage_exit
            ;;
    esac
done

if [ $OPT_ERROR ]; then
    usage_exit
    exit 1
fi

shift $(( $OPTIND - 1 ))

if [ "$ENV" != "dev" -a "$ENV" != "prod" ]; then
    usage_exit
    exit 1
fi

echo "$ENV へのデプロイ作業を開始します"

#==== デプロイ =====
echo "デプロイを開始します・・・。"
cd $PRJ_ROOT/app
sls deploy -s $ENV
echo "デプロイ完了"
