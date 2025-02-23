import concurrent.futures
import time

from quasi_utils.oms_utils import request

TEST_URL = 'https://api.kite.trade/portfolio/positions'
HEADERS = {'X-Kite-Version': '3', 'User-Agent': 'Kiteconnect-python/5.0.1',
           'Authorization': 'token 3uggvz253hhhfjnp:ck1DxwiPfxkY16cL4VOT5Foh1sXIXrzM'}


def test_request():
	time.sleep(0.2)

	start_time = time.time()
	res = request('GET', TEST_URL, headers=HEADERS, max_retries=1, retry_delay=1)
	end_time = time.time()
	
	return {'status_code': res.get('status_code', 'Unknown'), 'response_time': round(end_time - start_time, 4),
	        'response': res}


def load_test(num_requests=10, max_workers=5):
	results = []
	
	start_time = time.time()  # Overall test start time
	with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
		futures = [executor.submit(test_request) for _ in range(num_requests)]
		for future in concurrent.futures.as_completed(futures):
			results.append(future.result())  # Collect result of each request
	end_time = time.time()  # Overall test end time
	
	# Process statistics
	response_times = [r['response_time'] for r in results]
	success_count = sum(1 for r in results if r['status_code'] == 200)
	failure_count = num_requests - success_count
	avg_time = sum(response_times) / len(response_times) if response_times else 0
	min_time = min(response_times, default=0)
	max_time = max(response_times, default=0)
	
	# Print summary
	print('\n📊 Load Test Results:')
	print(f'🕒 Total Execution Time: {round(end_time - start_time, 4)} seconds')
	print(f'✅ Successful Requests: {success_count}/{num_requests}')
	print(f'❌ Failed Requests (Non-200): {failure_count}/{num_requests}')
	print(f'⏳ Avg Response Time: {avg_time:.4f} sec')
	print(f'🚀 Fastest Response: {min_time:.4f} sec')
	print(f'🐢 Slowest Response: {max_time:.4f} sec')
	
	# Print per-request details
	print('\n🔹 Individual Request Details:')
	for i, r in enumerate(results):
		print(f"🔹 Req {i + 1}: Response {r['response']}, Time {r['response_time']}s")


load_test(num_requests=60, max_workers=15)
