#!/bin/sh

source .env
npx @modelcontextprotocol/inspector \
  uv \
  --directory /Users/ouzhencong/Codes/assistants/longport-stock-server/src \
  run \
  longport_stock_server/main.py \
  --app-key $LONGPORT_APP_KEY \
  --app-secret $LONGPORT_APP_SECRET \
  --access-token $LONGPORT_ACCESS_TOKEN \
  --region "cn" \
  --enable-overnight true


