// Performance monitoring for render blocking resource optimization
// This script helps track Core Web Vitals and loading performance
/*global window, document, performance, console, PerformanceObserver, setTimeout */

(function () {
    'use strict';

    function PerformanceMonitor() {
        this.metrics = {};
        this.init();
    }

    PerformanceMonitor.prototype.init = function () {
        var self = this;

        // Monitor when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function () {
                self.measureDOMReady();
            });
        } else {
            this.measureDOMReady();
        }

        // Monitor when all resources are loaded
        window.addEventListener('load', function () {
            self.measurePageLoad();
            self.measureCoreWebVitals();
        });

        // Monitor CSS loading
        this.monitorCSSLoading();
    };

    PerformanceMonitor.prototype.measureDOMReady = function () {
        var body,
            computedStyle,
            hasGradient;

        this.metrics.domReady = performance.now();
        console.log('DOM Ready: ' + this.metrics.domReady.toFixed(2) + 'ms');

        // Check if critical styles are applied
        body = document.body;
        computedStyle = window.getComputedStyle(body);
        hasGradient = computedStyle.background.indexOf('gradient') !== -1;

        if (hasGradient) {
            console.log('✅ Critical CSS loaded successfully');
        } else {
            console.log('⚠️ Critical CSS may not be applied');
        }
    };

    PerformanceMonitor.prototype.measurePageLoad = function () {
        var navigation;

        this.metrics.pageLoad = performance.now();
        console.log('Page Load: ' + this.metrics.pageLoad.toFixed(2) + 'ms');

        // Measure resource loading times
        navigation = performance.getEntriesByType('navigation')[0];
        if (navigation) {
            console.log('DNS Lookup: ' + (navigation.domainLookupEnd - navigation.domainLookupStart).toFixed(2) + 'ms');
            console.log('TCP Connect: ' + (navigation.connectEnd - navigation.connectStart).toFixed(2) + 'ms');
            console.log('Response: ' + (navigation.responseEnd - navigation.responseStart).toFixed(2) + 'ms');
            console.log('DOM Processing: ' + (navigation.domContentLoadedEventEnd - navigation.responseEnd).toFixed(2) + 'ms');
        }
    };

    PerformanceMonitor.prototype.measureCoreWebVitals = function () {
        var self = this,
            clsValue = 0;

        // Largest Contentful Paint (LCP)
        new PerformanceObserver(function (entryList) {
            var entries = entryList.getEntries(),
                lastEntry = entries[entries.length - 1];

            self.metrics.lcp = lastEntry.startTime;
            console.log('LCP: ' + self.metrics.lcp.toFixed(2) + 'ms');

            if (self.metrics.lcp <= 2500) {
                console.log('✅ LCP is Good');
            } else if (self.metrics.lcp <= 4000) {
                console.log('⚠️ LCP needs improvement');
            } else {
                console.log('❌ LCP is Poor');
            }
        }).observe({ entryTypes: ['largest-contentful-paint'] });

        // First Input Delay (FID)
        new PerformanceObserver(function (entryList) {
            var entries = entryList.getEntries();
            entries.forEach(function (entry) {
                self.metrics.fid = entry.processingStart - entry.startTime;
                console.log('FID: ' + self.metrics.fid.toFixed(2) + 'ms');

                if (self.metrics.fid <= 100) {
                    console.log('✅ FID is Good');
                } else if (self.metrics.fid <= 300) {
                    console.log('⚠️ FID needs improvement');
                } else {
                    console.log('❌ FID is Poor');
                }
            });
        }).observe({ entryTypes: ['first-input'] });

        // Cumulative Layout Shift (CLS)
        new PerformanceObserver(function (entryList) {
            var entries = entryList.getEntries();
            entries.forEach(function (entry) {
                if (!entry.hadRecentInput) {
                    clsValue += entry.value;
                }
            });
            self.metrics.cls = clsValue;
            console.log('CLS: ' + self.metrics.cls.toFixed(3));

            if (self.metrics.cls <= 0.1) {
                console.log('✅ CLS is Good');
            } else if (self.metrics.cls <= 0.25) {
                console.log('⚠️ CLS needs improvement');
            } else {
                console.log('❌ CLS is Poor');
            }
        }).observe({ entryTypes: ['layout-shift'] });
    };

    PerformanceMonitor.prototype.monitorCSSLoading = function () {
        var cssLinks = document.querySelectorAll('link[rel="preload"][as="style"]'),
            loadedCount = 0;

        cssLinks.forEach(function (link, index) {
            var startTime = performance.now();

            function checkLoaded() {
                var loadTime;
                if (link.sheet || link.href.indexOf('font-awesome') !== -1) {
                    loadedCount += 1;
                    loadTime = performance.now() - startTime;
                    console.log('CSS Resource ' + (index + 1) + ' loaded: ' + loadTime.toFixed(2) + 'ms');

                    if (loadedCount === cssLinks.length) {
                        console.log('✅ All CSS resources loaded non-blocking');
                    }
                }
            }

            link.addEventListener('load', checkLoaded);
            // Fallback check
            setTimeout(checkLoaded, 100);
        });
    };

    PerformanceMonitor.prototype.getReport = function () {
        return {
            summary: 'Performance Optimization Results',
            metrics: this.metrics,
            recommendations: this.getRecommendations()
        };
    };

    PerformanceMonitor.prototype.getRecommendations = function () {
        var recommendations = [];

        if (this.metrics.lcp > 2500) {
            recommendations.push('Consider further optimizing LCP by reducing server response time or optimizing critical resources');
        }

        if (this.metrics.fid > 100) {
            recommendations.push('Reduce JavaScript execution time to improve FID');
        }

        if (this.metrics.cls > 0.1) {
            recommendations.push('Minimize layout shifts by reserving space for dynamic content');
        }

        return recommendations;
    };

    // Initialize performance monitoring
    if (window !== undefined) {
        window.performanceMonitor = new PerformanceMonitor();

        // Report results after page load
        window.addEventListener('load', function () {
            setTimeout(function () {
                console.log('\n=== Performance Report ===');
                console.log(window.performanceMonitor.getReport());
            }, 5000);
        });
    }

}());
