"""API latency testing command."""

import requests
import typer

from devpulse.core.formatter import print_error, print_latency_results
from devpulse.core.models import LatencyResult, LatencyStats
from devpulse.core.utils import parse_urls, timer


def test_url(url: str, timeout: int = 10) -> LatencyResult:
    """Test a single URL and measure latency.

    Args:
        url: URL to test
        timeout: Request timeout in seconds

    Returns:
        LatencyResult with timing and status information
    """
    try:
        with timer() as elapsed:
            response = requests.get(url, timeout=timeout)

        return LatencyResult(url=url, status_code=response.status_code, response_time_ms=elapsed[0])
    except requests.exceptions.Timeout:
        return LatencyResult(url=url, error="Timeout")
    except requests.exceptions.ConnectionError:
        return LatencyResult(url=url, error="Connection failed")
    except requests.exceptions.RequestException as e:
        return LatencyResult(url=url, error=str(e))
    except Exception as e:
        return LatencyResult(url=url, error=f"Unexpected error: {str(e)}")


def calculate_stats(results: list[LatencyResult]) -> LatencyStats | None:
    """Calculate statistics from latency results.

    Args:
        results: List of latency test results

    Returns:
        LatencyStats or None if no successful results
    """
    successful = [r for r in results if r.is_success and r.response_time_ms is not None]

    if not successful:
        return None

    times = [r.response_time_ms for r in successful]

    return LatencyStats(
        results=results,
        avg_latency_ms=sum(times) / len(times),
        fastest_ms=min(times),
        slowest_ms=max(times),
        success_count=len(successful),
        total_count=len(results),
    )


def latency_command(
    urls: str = typer.Argument(..., help="File path or comma-separated URLs to test"),
    timeout: int = typer.Option(10, "--timeout", "-t", help="Request timeout in seconds"),
) -> None:
    """Test API latency for multiple URLs.

    Examples:
        devpulse latency urls.txt
        devpulse latency "https://api1.com,https://api2.com"
        devpulse latency urls.txt --timeout 5
    """
    url_list = parse_urls(urls)

    if not url_list:
        print_error("No URLs provided")
        raise typer.Exit(1)

    results = []
    for url in url_list:
        result = test_url(url, timeout=timeout)
        results.append(result)

    stats = calculate_stats(results)

    if stats:
        print_latency_results(stats)
    else:
        print_error("All requests failed")
        for result in results:
            print_error(f"{result.url}: {result.error}")
        raise typer.Exit(1)
