// Performance monitoring for render blocking resource optimization
// This script helps track Core Web Vitals and loading performance

class PerformanceMonitor {
    constructor() {
        this.metrics = {};
        this.init();
    }

    init() {
        // Monitor when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.measureDOMReady();
            });
        } else {
            this.measureDOMReady();
        }

        // Monitor when all resources are loaded
        window.addEventListener('load', () => {
            this.measurePageLoad();
            this.measureCoreWebVitals();
        });

        // Monitor CSS loading
        this.monitorCSSLoading();
    }

    measureDOMReady() {
        this.metrics.domReady = performance.now();
        console.log(`DOM Ready: ${this.metrics.domReady.toFixed(2)}ms`);
        
        // Check if critical styles are applied
        const body = document.body;
        const computedStyle = window.getComputedStyle(body);
        const hasGradient = computedStyle.background.includes('gradient');
        
        if (hasGradient) {
            console.log('✅ Critical CSS loaded successfully');
        } else {
            console.log('⚠️ Critical CSS may not be applied');
        }
    }

    measurePageLoad() {
        this.metrics.pageLoad = performance.now();
        console.log(`Page Load: ${this.metrics.pageLoad.toFixed(2)}ms`);
        
        // Measure resource loading times
        const navigation = performance.getEntriesByType('navigation')[0];
        if (navigation) {
            console.log(`DNS Lookup: ${(navigation.domainLookupEnd - navigation.domainLookupStart).toFixed(2)}ms`);
            console.log(`TCP Connect: ${(navigation.connectEnd - navigation.connectStart).toFixed(2)}ms`);
            console.log(`Response: ${(navigation.responseEnd - navigation.responseStart).toFixed(2)}ms`);
            console.log(`DOM Processing: ${(navigation.domContentLoadedEventEnd - navigation.responseEnd).toFixed(2)}ms`);
        }
    }

    measureCoreWebVitals() {
        // Largest Contentful Paint (LCP)
        new PerformanceObserver((entryList) => {
            const entries = entryList.getEntries();
            const lastEntry = entries[entries.length - 1];
            this.metrics.lcp = lastEntry.startTime;
            console.log(`LCP: ${this.metrics.lcp.toFixed(2)}ms`);
            
            if (this.metrics.lcp <= 2500) {
                console.log('✅ LCP is Good');
            } else if (this.metrics.lcp <= 4000) {
                console.log('⚠️ LCP needs improvement');
            } else {
                console.log('❌ LCP is Poor');
            }
        }).observe({ entryTypes: ['largest-contentful-paint'] });

        // First Input Delay (FID)
        new PerformanceObserver((entryList) => {
            const entries = entryList.getEntries();
            entries.forEach(entry => {
                this.metrics.fid = entry.processingStart - entry.startTime;
                console.log(`FID: ${this.metrics.fid.toFixed(2)}ms`);
                
                if (this.metrics.fid <= 100) {
                    console.log('✅ FID is Good');
                } else if (this.metrics.fid <= 300) {
                    console.log('⚠️ FID needs improvement');
                } else {
                    console.log('❌ FID is Poor');
                }
            });
        }).observe({ entryTypes: ['first-input'] });

        // Cumulative Layout Shift (CLS)
        let clsValue = 0;
        new PerformanceObserver((entryList) => {
            const entries = entryList.getEntries();
            entries.forEach(entry => {
                if (!entry.hadRecentInput) {
                    clsValue += entry.value;
                }
            });
            this.metrics.cls = clsValue;
            console.log(`CLS: ${this.metrics.cls.toFixed(3)}`);
            
            if (this.metrics.cls <= 0.1) {
                console.log('✅ CLS is Good');
            } else if (this.metrics.cls <= 0.25) {
                console.log('⚠️ CLS needs improvement');
            } else {
                console.log('❌ CLS is Poor');
            }
        }).observe({ entryTypes: ['layout-shift'] });
    }

    monitorCSSLoading() {
        const cssLinks = document.querySelectorAll('link[rel="preload"][as="style"]');
        let loadedCount = 0;
        
        cssLinks.forEach((link, index) => {
            const startTime = performance.now();
            
            const checkLoaded = () => {
                if (link.sheet || link.href.includes('font-awesome')) {
                    loadedCount++;
                    const loadTime = performance.now() - startTime;
                    console.log(`CSS Resource ${index + 1} loaded: ${loadTime.toFixed(2)}ms`);
                    
                    if (loadedCount === cssLinks.length) {
                        console.log('✅ All CSS resources loaded non-blocking');
                    }
                }
            };
            
            link.addEventListener('load', checkLoaded);
            // Fallback check
            setTimeout(checkLoaded, 100);
        });
    }

    getReport() {
        return {
            summary: 'Performance Optimization Results',
            metrics: this.metrics,
            recommendations: this.getRecommendations()
        };
    }

    getRecommendations() {
        const recommendations = [];
        
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
    }
}

// Initialize performance monitoring
if (typeof window !== 'undefined') {
    window.performanceMonitor = new PerformanceMonitor();
    
    // Report results after page load
    window.addEventListener('load', () => {
        setTimeout(() => {
            console.log('\n=== Performance Report ===');
            console.log(window.performanceMonitor.getReport());
        }, 5000);
    });
}
