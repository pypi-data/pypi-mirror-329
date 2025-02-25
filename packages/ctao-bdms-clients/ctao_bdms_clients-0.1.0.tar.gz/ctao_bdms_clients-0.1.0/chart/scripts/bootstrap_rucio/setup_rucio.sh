#!/bin/bash

set -eux -o pipefail

# copy user certs to fix permissions
# cp /tmp/userkey.pem /tmp/usercert.pem /opt/rucio/etc/
# chmod 600 /opt/rucio/etc/userkey.pem
voms-proxy-init -valid 9999:00 -cert /opt/rucio/etc/usercert.pem -key /opt/rucio/etc/userkey.pem -out /tmp/x509up
cp -fv /tmp/x509up /tmp/x509up_u$(id -u)

rucio-admin identity add --type X509 \
      --id "CN=DPPS User" \
      --email dpps-test@cta-observatory.org --account root


# add the storage element (xrd)
for N in 1 2 3; do
  rucio-admin rse add "STORAGE-${N}"
  rucio-admin rse add-protocol \
      --hostname "rucio-storage-$N" --scheme root --prefix //rucio --port 1094 \
      --impl rucio.rse.protocols.gfal.Default \
      --domain-json '{"wan": {"read": 1, "write": 1, "delete": 1, "third_party_copy_read": 1, "third_party_copy_write": 1}, "lan": {"read": 1, "write": 1, "delete": 1}}' \
      "STORAGE-${N}"

  rucio-admin rse set-attribute --rse "STORAGE-${N}" --key fts --value https://${HELM_RELEASE_NAME}-fts:8446

  # this RSE attribute is currently required for the rucio-dirac integration, see https://github.com/rucio/rucio/issues/6852
  rucio-admin rse set-attribute --rse "STORAGE-${N}" --key ANY --value true

  # set quota
  rucio-admin account set-limits root "STORAGE-${N}" -1
done

# All RSEs connected to all other RSEs directly for now
for A in 1 2 3; do
  for B in 1 2 3; do
    [ $A == $B ] && continue
    rucio-admin rse add-distance --distance 1 --ranking 1 STORAGE-$A STORAGE-$B
  done
done

# add a scope
rucio-admin scope add --account root --scope root
# the root container for the VO already needs to exist
rucio add-container /ctao.dpps.test

# verify connection to the FTS, and delegate a proxy
# TODO: should this be moved to a different job with a different image?

while true; do
  if curl -v https://${HELM_RELEASE_NAME}-fts:8446; then
    echo "FTS is up"
    break
  fi
  echo "FTS is not up, retrying in 5 seconds"
  sleep 5
done

curl -v https://${HELM_RELEASE_NAME}-fts:8446

fts-rest-whoami --capath /etc/grid-security/certificates --cert /opt/rucio/etc/usercert.pem --key /opt/rucio/etc/userkey.pem  -s https://${HELM_RELEASE_NAME}-fts:8446
fts-rest-delegate --capath /etc/grid-security/certificates --cert /opt/rucio/etc/usercert.pem --key /opt/rucio/etc/userkey.pem -vf -s https://${HELM_RELEASE_NAME}-fts:8446 -H 9999
