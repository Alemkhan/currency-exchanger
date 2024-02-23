# Currency Conversion Service
## How to launch
Please provide a `.env` file so that docker-compose could run successfully. You can appeal to `.env.example` file.

After environment variables are filled in `.env` file run docker-compose file via `docker-compose up` command

## How to use
There are 3 main endpoints:
1. `/api/v1/rates/rates-last-update-date` - this returns the date the last rate update is made
2. `/api/v1/rates/convert-money` - provides a convert logic to a user (if no currency provided or there is no one of the currencies the error will be raised)
3. `/api/v1/rates/update` - provides a functionality to update rates inplace not to wait till the task will run