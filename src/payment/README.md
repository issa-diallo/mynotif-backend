# Configuring the Stripe Webhook Locally

This guide explains how to configure and activate the Stripe webhook in your local development environment.

## Prerequisites

- Have a Stripe account
- Have the Stripe CLI installed
- A local server running on port 8000

## Configuration Steps

### 1. Connecting to Stripe

Start by logging into your Stripe account via the CLI:

```bash
stripe login
```

Once logged in, you will receive a confirmation message similar to:

```bash
Please note: this key will expire after 90 days, at which point you'll need to re-authenticate.
```

### 2. Starting the Webhook

Start listening to the webhook with the following command:

```bash
stripe listen --forward-to http://localhost:8000/api/v1/payment/stripe/webhook/
```

If successful, the CLI will display:

The Stripe version
A webhook secret key (example):

```bash
whsec_32fe6a41dfc322a72691c09bb18a6af91234c496e7bb8884b22cac570e495987z
```

### 3. Environment Configuration

Add the webhook secret key to your .env file:

## Important Notes

- The Stripe connection key expires after 90 days
- Keep your webhook secret key confidential
- Ensure your local server is running on port 8000 before starting the webhook

## Troubleshooting

If you encounter issues:

- Verify that your local server is running
- Ensure port 8000 is available
- Confirm that your Stripe key is still valid
