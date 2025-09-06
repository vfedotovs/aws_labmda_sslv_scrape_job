# API Documentation

## Lambda Function Interface

### Handler Function
```python
def handler(event, context):
    """
    Main Lambda entry point for SSLV scraper
    
    Args:
        event (dict): Lambda event object (currently unused)
        context (LambdaContext): Lambda context object
        
    Returns:
        dict: Response with status and message
    """
```

### Response Format
```json
{
    "status": "True",
    "statusCode": 200,
    "body": "File with scraped data was uploaded to S3 bucket successfully"
}
```

## Data Scraping Functions

### `find_single_page_urls(bs_object)`
Extracts message URLs from BeautifulSoup object.

**Parameters:**
- `bs_object`: BeautifulSoup parsed HTML object

**Returns:**
- `list`: List of unique message URLs

### `extract_data_from_url(nondup_urls)`
Scrapes data from each message URL and writes to file.

**Parameters:**
- `nondup_urls`: List of unique message URLs

**Side Effects:**
- Creates local file: `Ogre-raw-data-report.txt`
- Writes scraped data to file

### `get_msg_table_info(msg_url, td_class)`
Extracts specific table field data from message page.

**Parameters:**
- `msg_url`: Message web page URL
- `td_class`: CSS class name for table field

**Returns:**
- `list`: List of extracted field values

## S3 Integration

### `upload_text_file_to_s3(file_path, bucket_name, s3_key)`
Uploads scraped data file to S3 bucket.

**Parameters:**
- `file_path`: Local file path
- `bucket_name`: S3 bucket name
- `s3_key`: S3 object key

### `add_datetime_to_filename(filename)`
Adds timestamp to filename for uniqueness.

**Parameters:**
- `filename`: Original filename

**Returns:**
- `str`: Filename with timestamp suffix

## Data Structure

### Scraped Data Format
The scraper extracts the following data for each apartment:

```
Message URL
Field Name>Field Value
Field Name>Field Value
...
Price>Price Value
Date>Date Value
```

### Example Output
```
https://ss.lv/msg/lv/real-estate/flats/ogre-and-reg/ogre/dlonf.html
Room count>2
Area>45
Floor>3
Price>45000
Date>2023-02-18
```

## Error Handling

### Common Error Scenarios
1. **Network timeouts**: Retry logic with exponential backoff
2. **Invalid URLs**: Skip malformed URLs and continue
3. **S3 upload failures**: Log error and return failure status
4. **Rate limiting**: Built-in 2-second delay between requests

### Error Response Format
```json
{
    "status": "False",
    "statusCode": 500,
    "body": "Error message describing the failure"
}
```

## Performance Considerations

### Execution Time
- **Typical duration**: 3-4 minutes
- **Timeout setting**: 15 minutes (900 seconds)
- **Memory allocation**: 512 MB

### Rate Limiting
- **Delay between requests**: 2 seconds
- **Pages scraped**: Up to 3 pages per city
- **Max ads per page**: ~30 ads

### Resource Usage
- **CPU**: Moderate (web scraping and parsing)
- **Memory**: Low (text processing)
- **Network**: High (multiple HTTP requests)

## Monitoring and Logging

### CloudWatch Logs
All function execution is logged to CloudWatch with:
- Start/end timestamps
- Progress updates
- Error messages
- S3 upload confirmations

### Key Metrics to Monitor
- Function duration
- Memory usage
- Error rate
- S3 upload success rate
