## Presequisites:
- saml2aws
- aws

## Preinstall

Recommendation: You should have installed and configured saml2aws and awscli before running the following steps.

## Install


```bash
pip install pd-cli
```

After that you should run (Push Notification as default MFA):
```bash
pd-cli login
```
You also can run the following command to set the MFA Option as Passcode:
```bash
pd-cli login --duo-mfa-option Passcode
```

Then you can run:
```bash
pd-cli config
```
to set all the connections. You must input the AWS Secret Manager ARN.


Congrats! you are ready to use pd-cli connect. Happy coding!


## Use

#### pd-cli login

pd-cli login command trigger a `saml2aws login` with the mfa option setup

usage:
```bash
pd-cli login
```

#### pd-cli connect

pd-cli connect allow you access to the services you have configured.

usage:
```bash
pd-cli connect
```

