const isLocal = window.location.hostname === 'localhost' ||
                window.location.hostname === '127.0.0.1';

const API_URL = isLocal
    ? 'http://localhost:5000'
    : 'https://PLACEHOLDER.execute-api.us-east-1.amazonaws.com';

const DATA_START_DATE = '2015-01-01';
const NUCLEAR_END_DATE = '2023-04-16';