# Utility Package Structure and Components

The `utils` package provides core utility functions used throughout the application, centralised to avoid duplication and ensure consistency. This document outlines the structure and purpose of each module within the `utils` package.

## Core Utilities

| Module | Function | Description |
|--------|----------|-------------|
| core.py | is_none_or_empty | Check if value is None or empty |
| core.py | ensure_list | Ensure value is a list |
| core.py | merge_dicts | Merge multiple dictionaries |
| core.py | deep_copy | Deep copy an object |
| core.py | generate_id | Generate unique identifier |
| core.py | chunk_list | Split list into chunks |
| core.py | flatten_list | Flatten nested lists |
| core.py | limit_string_length | Limit string length with ellipsis |
| core.py | remove_duplicates | Remove duplicates while preserving order |
| core.py | get_class_name | Get class name from instance |
| core.py | get_function_name | Get current function name |
| core.py | is_iterable | Check if object is iterable |

## Text Formatting and Processing

| Module | Function | Description |
|--------|----------|-------------|
| formatting.py | format_number | Format number with commas, precision |
| formatting.py | format_currency | Format number as currency |
| formatting.py | format_percentage | Format number as percentage |
| formatting.py | format_list | Format list as string with separators |
| formatting.py | format_duration | Format seconds as duration string |
| formatting.py | format_datetime | Format datetime with specified format |
| formatting.py | format_file_size | Format bytes as human-readable size |
| formatting.py | format_plural | Handle plural forms based on count |
| formatting.py | format_table | Format data as text table |
| formatting.py | format_progress_bar | Create text-based progress bar |
| formatting.py | truncate | Truncate text with ellipsis |
| formatting.py | wrap_text | Wrap text to specified width |
| formatting.py | indent_text | Indent text by specified amount |
| formatting.py | strip_formatting | Remove formatting characters |
| formatting.py | normalise_whitespace | Normalise whitespace in string |
| formatting.py | normalise_line_endings | Normalise line endings |
| formatting.py | escape_markdown | Escape markdown special characters |
| formatting.py | unescape_markdown | Unescape markdown special characters |

## Input Parsing and Validation

| Module | Function | Description |
|--------|----------|-------------|
| parsing.py | parse_command | Parse raw command from text |
| parsing.py | parse_arguments | Parse arguments from text |
| parsing.py | parse_key_value_pairs | Parse key-value pairs from text |
| parsing.py | parse_list | Parse comma-separated list from text |
| parsing.py | parse_bool | Parse boolean from string |
| parsing.py | parse_duration | Parse duration string to seconds |
| parsing.py | parse_date | Parse date string to date object |
| parsing.py | parse_time | Parse time string to time object |
| parsing.py | parse_datetime | Parse datetime string to datetime |
| parsing.py | parse_file_size | Parse file size string to bytes |
| parsing.py | extract_urls | Extract URLs from text |
| parsing.py | extract_mentions | Extract user mentions from text |
| parsing.py | extract_hashtags | Extract hashtags from text |
| parsing.py | extract_emotes | Extract emotes from text |
| parsing.py | split_on_delimiter | Split string on delimiter |
| parsing.py | tokenise | Tokenise string into words |

## Validation

| Module | Function | Description |
|--------|----------|-------------|
| validation.py | validate_type | Validate value is of specified type |
| validation.py | validate_not_none | Validate value is not None |
| validation.py | validate_not_empty | Validate value is not empty |
| validation.py | validate_length | Validate string length |
| validation.py | validate_range | Validate number in range |
| validation.py | validate_email | Validate email address format |
| validation.py | validate_url | Validate URL format |
| validation.py | validate_regex | Validate string against regex pattern |
| validation.py | validate_choice | Validate value in choices |
| validation.py | validate_schema | Validate data against schema |
| validation.py | validate_json | Validate JSON string |
| validation.py | validate_datetime | Validate datetime format |
| validation.py | validate_file_exists | Validate file exists |
| validation.py | validate_directory_exists | Validate directory exists |
| validation.py | validate_writable | Validate path is writable |
| validation.py | validate_readable | Validate path is readable |
| validation.py | validate_executable | Validate file is executable |
| validation.py | validate_function | Validate with custom function |

## Security and Sanitisation

| Module | Function | Description |
|--------|----------|-------------|
| security.py | generate_secure_token | Generate cryptographically secure token |
| security.py | hash_password | Securely hash password |
| security.py | verify_password | Verify password against hash |
| security.py | encrypt_data | Encrypt data |
| security.py | decrypt_data | Decrypt data |
| security.py | sanitise_filename | Sanitise filename for safe storage |
| security.py | sanitise_path | Sanitise path to prevent traversal |
| security.py | sanitise_html | Remove dangerous HTML |
| security.py | sanitise_sql | Sanitise against SQL injection |
| security.py | sanitise_command | Sanitise command arguments |
| security.py | sanitise_user_input | General user input sanitisation |
| security.py | mask_sensitive_data | Mask sensitive data for logging |
| security.py | is_valid_oauth_token | Validate OAuth token format |
| security.py | is_safe_string | Check if string contains unsafe characters |
| security.py | rate_limit_key | Generate key for rate limiting |
| security.py | generate_hmac | Generate HMAC signature |
| security.py | verify_hmac | Verify HMAC signature |

## Time-Related Utilities

| Module | Function | Description |
|--------|----------|-------------|
| time.py | get_current_timestamp | Get current timestamp |
| time.py | get_current_datetime | Get current datetime object |
| time.py | get_utc_now | Get current UTC datetime |
| time.py | to_utc | Convert datetime to UTC |
| time.py | to_local | Convert datetime to local timezone |
| time.py | parse_iso_datetime | Parse ISO 8601 datetime string |
| time.py | format_iso_datetime | Format datetime as ISO 8601 string |
| time.py | get_time_difference | Get time difference between two times |
| time.py | add_time | Add time delta to datetime |
| time.py | subtract_time | Subtract time delta from datetime |
| time.py | is_same_day | Check if two datetimes are same day |
| time.py | is_business_day | Check if date is business day |
| time.py | get_next_business_day | Get next business day from date |
| time.py | get_start_of_day | Get start of day datetime |
| time.py | get_end_of_day | Get end of day datetime |
| time.py | get_start_of_month | Get start of month datetime |
| time.py | get_end_of_month | Get end of month datetime |
| time.py | sleep | Asynchronous sleep function |
| time.py | with_timeout | Execute function with timeout |

## Random Utilities

| Module | Function | Description |
|--------|----------|-------------|
| random.py | random_string | Generate random string |
| random.py | random_int | Generate random integer in range |
| random.py | random_float | Generate random float in range |
| random.py | random_bool | Generate random boolean |
| random.py | random_choice | Select random item from list |
| random.py | random_choices | Select multiple random items |
| random.py | random_sample | Sample without replacement |
| random.py | weighted_choice | Select item based on weights |
| random.py | shuffled | Return shuffled copy of sequence |
| random.py | random_date | Generate random date in range |
| random.py | random_time | Generate random time |
| random.py | random_datetime | Generate random datetime in range |
| random.py | generate_seed | Generate random seed |
| random.py | set_seed | Set random seed |
| random.py | calculate_probability | Check if random event occurs |

## File System Utilities

| Module | Function | Description |
|--------|----------|-------------|
| file.py | read_file | Read file contents |
| file.py | write_file | Write content to file |
| file.py | append_file | Append content to file |
| file.py | file_exists | Check if file exists |
| file.py | directory_exists | Check if directory exists |
| file.py | create_directory | Create directory if not exists |
| file.py | delete_file | Delete file safely |
| file.py | delete_directory | Delete directory safely |
| file.py | list_files | List files in directory |
| file.py | list_directories | List directories in directory |
| file.py | get_file_size | Get file size |
| file.py | get_file_hash | Calculate file hash |
| file.py | get_file_extension | Get file extension |
| file.py | change_extension | Change file extension |
| file.py | normalize_path | Normalize path separators |
| file.py | get_absolute_path | Get absolute path |
| file.py | get_relative_path | Get relative path |
| file.py | join_paths | Join path components safely |
| file.py | get_temp_path | Get temporary file/directory path |

## Threading and Concurrency

| Module | Function | Description |
|--------|----------|-------------|
| concurrency.py | run_in_thread | Run function in separate thread |
| concurrency.py | run_in_threadpool | Run function in thread pool |
| concurrency.py | run_in_process | Run function in separate process |
| concurrency.py | run_in_executor | Run blocking function in executor |
| concurrency.py | run_concurrently | Run multiple coroutines concurrently |
| concurrency.py | gather_with_concurrency | Gather with concurrency limit |
| concurrency.py | debounce | Debounce function calls |
| concurrency.py | throttle | Throttle function calls |
| concurrency.py | with_retry | Retry function on failure |
| concurrency.py | with_backoff | Retry with exponential backoff |
| concurrency.py | cancel_after | Cancel coroutine after timeout |
| concurrency.py | shield | Shield coroutine from cancellation |
| concurrency.py | wait_for_event | Wait for event with timeout |
| concurrency.py | periodic | Run function periodically |

## Collections and Data Structures

| Module | Function | Description |
|--------|----------|-------------|
| collections.py | cached_property | Property with caching |
| collections.py | LRUCache | Least Recently Used Cache |
| collections.py | ExpiringCache | Cache with expiring entries |
| collections.py | PriorityQueue | Thread-safe priority queue |
| collections.py | CircularBuffer | Fixed-size circular buffer |
| collections.py | DefaultOrderedDict | OrderedDict with default factory |
| collections.py | frozen_dict | Immutable dictionary |
| collections.py | AttrDict | Dictionary accessible via attributes |
| collections.py | group_by | Group items by key function |
| collections.py | partition | Partition items into two lists |
| collections.py | pairs | Iterate over pairs in sequence |
| collections.py | window | Sliding window over sequence |
| collections.py | find | Find item in sequence |
| collections.py | find_all | Find all matching items |
| collections.py | index_of | Get index of item in sequence |
| collections.py | count_by | Count items by key function |

## Math Utilities

| Module | Function | Description |
|--------|----------|-------------|
| math.py | clamp | Clamp value between min/max |
| math.py | lerp | Linear interpolation |
| math.py | map_range | Map value from one range to another |
| math.py | round_to_nearest | Round to nearest multiple |
| math.py | is_power_of_two | Check if number is power of two |
| math.py | next_power_of_two | Get next power of two |
| math.py | mean | Calculate arithmetic mean |
| math.py | median | Calculate median value |
| math.py | mode | Calculate mode value(s) |
| math.py | percentile | Calculate percentile |
| math.py | standard_deviation | Calculate standard deviation |
| math.py | variance | Calculate variance |
| math.py | moving_average | Calculate moving average |
| math.py | weighted_average | Calculate weighted average |
| math.py | distance | Calculate distance between points |
| math.py | normalise | Normalise values in collection |

## System Utilities

| Module | Function | Description |
|--------|----------|-------------|
| system.py | get_cpu_count | Get number of CPU cores |
| system.py | get_cpu_usage | Get current CPU usage |
| system.py | get_memory_usage | Get current memory usage |
| system.py | get_disk_usage | Get disk usage for path |
| system.py | get_platform_info | Get platform information |
| system.py | get_python_version | Get Python version |
| system.py | get_process_id | Get current process ID |
| system.py | kill_process | Kill process by ID |
| system.py | is_process_running | Check if process is running |
| system.py | get_environment_variable | Get environment variable |
| system.py | set_environment_variable | Set environment variable |
| system.py | run_command | Run system command |
| system.py | get_command_output | Get output from command |
| system.py | is_admin | Check if running as administrator |
| system.py | get_ip_address | Get machine IP address |
| system.py | get_hostname | Get machine hostname |

## Network Utilities

| Module | Function | Description |
|--------|----------|-------------|
| network.py | ping | Ping host |
| network.py | is_port_open | Check if port is open |
| network.py | get_free_port | Get available port |
| network.py | download_file | Download file from URL |
| network.py | get_public_ip | Get public IP address |
| network.py | is_valid_ip | Validate IP address |
| network.py | is_valid_port | Validate port number |
| network.py | encode_url_params | Encode URL parameters |
| network.py | decode_url_params | Decode URL parameters |
| network.py | parse_url | Parse URL into components |
| network.py | build_url | Build URL from components |
| network.py | url_join | Join URL components |
| network.py | is_url_reachable | Check if URL is reachable |
| network.py | get_domain_from_url | Extract domain from URL |
| network.py | get_path_from_url | Extract path from URL |

## Feature-Specific Utilities

| Module | Function | Description |
|--------|----------|-------------|
| twitch.py | format_username | Format Twitch username |
| twitch.py | normalise_username | Normalise Twitch username |
| twitch.py | is_valid_username | Validate Twitch username |
| twitch.py | parse_twitch_badge | Parse Twitch badge info |
| twitch.py | parse_twitch_emotes | Parse Twitch emote data |
| twitch.py | get_twitch_emote_url | Get URL for Twitch emote |
| obs.py | validate_scene_name | Validate OBS scene name |
| obs.py | validate_source_name | Validate OBS source name |
| obs.py | validate_filter_name | Validate OBS filter name |
| obs.py | format_obs_request | Format OBS WebSocket request |
| obs.py | parse_obs_response | Parse OBS WebSocket response |
| points.py | format_points | Format points value |
| points.py | calculate_points_reward | Calculate points reward |
| points.py | validate_points_transaction | Validate points transaction |
| duel.py | calculate_win_probability | Calculate duel win probability |
| duel.py | format_duel_result | Format duel result message |
| duel.py | create_duel_id | Generate unique duel ID |