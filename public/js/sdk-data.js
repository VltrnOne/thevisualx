// VLTRN SDK Tools Data
const SDK_DATA = [
    {
        id: 'trading-sdk',
        name: 'vltrn-trading-sdk',
        category: 'Trading',
        status: 'ready',
        language: 'Python',
        price: 499,
        description: 'Production-ready algorithmic trading engine with position tracking, circuit breakers, and automated exit management. Battle-tested with 1,200+ trades over 8 months.',
        examples: [
            {
                title: 'Automated Trading with Safety Limits',
                description: 'Set up a trading strategy with take-profit, trailing stops, and daily spending caps to protect your capital.'
            },
            {
                title: 'Auto-Sell with Peak Tracking',
                description: 'Automatically exit positions based on profit targets, trailing stops, or maximum hold time.'
            }
        ],
        features: [
            'Position tracking with atomic persistence',
            'Circuit breakers (daily spend/loss caps)',
            'Automated exit management',
            'Real-time P&L calculation',
            '30 test cases, 7 CLI commands'
        ],
        stats: {
            trades: '1,200+',
            uptime: '99.7%',
            incidents: '0'
        }
    },
    {
        id: 'position-tracker',
        name: 'vltrn-position-tracker',
        category: 'Trading',
        status: 'ready',
        language: 'Python',
        price: 399,
        description: 'Atomic position tracking with crash-safe persistence, real-time P&L calculation, and support for fractional exits. Perfect for managing multi-token portfolios.',
        examples: [
            {
                title: 'Track Multiple Positions',
                description: 'Monitor multiple token positions with average entry price and total holdings across your portfolio.'
            },
            {
                title: 'Fractional Sells with P&L',
                description: 'Sell portions of positions while automatically calculating realized profits and remaining holdings.'
            }
        ],
        features: [
            'Atomic JSON persistence',
            'Average entry price tracking',
            'Fractional exit support',
            '25 test cases, 7 CLI commands'
        ]
    },
    {
        id: 'circuit-breakers',
        name: 'vltrn-circuit-breakers',
        category: 'Trading',
        status: 'ready',
        language: 'Python',
        price: 399,
        description: 'Trading safety system with daily spend and loss caps, automatic reset at midnight, and atomic persistence. Prevented $3,200+ in losses during production use.',
        examples: [
            {
                title: 'Enforce Daily Limits',
                description: 'Prevent runaway losses by setting maximum daily spending and loss thresholds.'
            },
            {
                title: 'Loss Cap Protection',
                description: 'Automatically halt trading when daily loss limits are breached for capital protection.'
            }
        ],
        features: [
            'Daily spend caps',
            'Daily loss caps',
            'Auto-reset at midnight',
            '27 test cases, 7 CLI commands'
        ],
        stats: {
            saved: '$3,200+',
            incidents: '0'
        }
    },
    {
        id: 'jwt-auth',
        name: '@vltrn/jwt-auth-middleware',
        category: 'Auth',
        status: 'ready',
        language: 'Node.js',
        price: 299,
        description: 'Complete JWT authentication system with bcrypt password hashing, Express middleware, and role-based access control. 5,200+ tokens issued with zero security breaches.',
        examples: [
            {
                title: 'Protect API Routes',
                description: 'Secure your Express API endpoints with JWT authentication and automatic token validation.'
            },
            {
                title: 'Role-Based Access',
                description: 'Implement granular permissions with role-based middleware for admin, user, and custom roles.'
            }
        ],
        features: [
            'bcrypt password hashing',
            'JWT generation & verification',
            'Express middleware',
            'Role-based access control',
            '39 test cases, 4 CLI commands'
        ],
        stats: {
            tokens: '5,200+',
            breaches: '0'
        }
    },
    {
        id: 'session-manager',
        name: '@vltrn/session-manager',
        category: 'Auth',
        status: 'ready',
        language: 'Node.js',
        price: 199,
        description: 'Redis-backed session management with automatic expiry, sliding expiration, and Express middleware integration. Perfect for multi-tenant applications.',
        examples: [
            {
                title: 'Session with Auto-Expiry',
                description: 'Automatically expire inactive sessions while extending active ones with sliding expiration.'
            },
            {
                title: 'Multi-Tenant Sessions',
                description: 'Isolate sessions by tenant with prefix-based session keys for SaaS applications.'
            }
        ],
        features: [
            'Redis-backed storage',
            'Automatic expiry',
            'Sliding expiration',
            '20+ test cases, 4 CLI commands'
        ]
    },
    {
        id: 'eventbus',
        name: 'vltrn-eventbus',
        category: 'Infrastructure',
        status: 'ready',
        language: 'Python',
        price: 199,
        description: 'Zero-dependency broadcast event bus with 10,000+ events/sec throughput. Perfect for microservices communication and real-time event distribution.',
        examples: [
            {
                title: 'Microservices Communication',
                description: 'Enable loose coupling between services with publish-subscribe event patterns.'
            },
            {
                title: 'WebSocket Fanout',
                description: 'Broadcast updates to all connected WebSocket clients with minimal latency.'
            }
        ],
        features: [
            'Zero dependencies',
            '10,000+ events/sec',
            'asyncio pub-sub',
            '22 test cases, 4 CLI commands'
        ],
        stats: {
            throughput: '10,000+/sec',
            dependencies: '0'
        }
    },
    {
        id: 'atomic',
        name: 'vltrn-atomic',
        category: 'Infrastructure',
        status: 'ready',
        language: 'Python',
        price: 149,
        description: '50-line crash-safe atomic file writer with zero dependencies. Uses temp file + atomic rename to prevent corruption on crashes.',
        examples: [
            {
                title: 'Crash-Safe Config Files',
                description: 'Update configuration files safely with guaranteed atomicity even during system crashes.'
            },
            {
                title: 'Concurrent Writes',
                description: 'Handle multiple processes writing to files without data corruption or race conditions.'
            }
        ],
        features: [
            '50-line implementation',
            'Zero dependencies',
            'Cross-platform',
            '20+ test cases'
        ],
        stats: {
            size: '50 lines',
            dependencies: '0'
        }
    },
    {
        id: 'rate-limiter',
        name: '@vltrn/rate-limiter',
        category: 'Infrastructure',
        status: 'ready',
        language: 'Node.js',
        price: 199,
        description: 'Express middleware for API rate limiting with Redis store, 10+ presets, and tiered limits. Includes burst protection and per-user limits.',
        examples: [
            {
                title: 'API Endpoint Protection',
                description: 'Apply pre-configured rate limits to public, authenticated, and premium API endpoints.'
            },
            {
                title: 'Custom Tiered Limits',
                description: 'Create custom rate limits based on user subscription tiers (free, pro, enterprise).'
            }
        ],
        features: [
            'Express middleware',
            'Redis store',
            '10+ presets',
            '20+ test cases'
        ]
    },
    {
        id: 'stripe-webhook',
        name: '@vltrn/stripe-webhook-handler',
        category: 'APIs',
        status: 'ready',
        language: 'Node.js',
        price: 299,
        description: 'Production-ready Stripe webhook handler with signature verification, event routing, and idempotency. Processed 340+ users with 45ms avg response.',
        examples: [
            {
                title: 'Subscription Management',
                description: 'Automatically handle subscription lifecycle events like creation, cancellation, and payment failures.'
            },
            {
                title: 'CRM Sync with Idempotency',
                description: 'Sync customer data to your CRM with guaranteed once-only processing via idempotency keys.'
            }
        ],
        features: [
            'Signature verification',
            'Event routing',
            'Idempotency',
            '34 test cases'
        ],
        stats: {
            users: '340+',
            response: '45ms'
        }
    },
    {
        id: 'solana-rpc',
        name: '@vltrn/solana-rpc-client',
        category: 'APIs',
        status: 'ready',
        language: 'Node.js',
        price: 399,
        description: 'Production-grade Solana RPC client with Helius primary, automatic fallback, retry logic, and WebSocket subscriptions. 99.97% uptime.',
        examples: [
            {
                title: 'Transaction with Auto-Retry',
                description: 'Send transactions with automatic retry on failure and fallback to backup RPC endpoints.'
            },
            {
                title: 'Real-Time Token Monitoring',
                description: 'Subscribe to token events and account changes via WebSocket with automatic reconnection.'
            }
        ],
        features: [
            'Helius RPC primary',
            'Fallback chain',
            'WebSocket subscriptions',
            '20+ test cases'
        ],
        stats: {
            uptime: '99.97%',
            response: '180ms'
        }
    },
    {
        id: 'telegram-alerts',
        name: '@vltrn/telegram-alerts',
        category: 'APIs',
        status: 'ready',
        language: 'Node.js',
        price: 149,
        description: 'Telegram Bot API integration with 7 pre-built templates, rate limiting, and HTML/Markdown support. Delivered 5,000+ alerts.',
        examples: [
            {
                title: 'Trading Alerts',
                description: 'Send formatted trading notifications with buy/sell actions, prices, and P&L calculations.'
            },
            {
                title: 'Error Monitoring',
                description: 'Automatically send error alerts to Telegram with stack traces and rate limiting.'
            }
        ],
        features: [
            '7 templates',
            'Rate limiting',
            'HTML/Markdown',
            '20+ test cases'
        ],
        stats: {
            alerts: '5,000+',
            delivery: '320ms'
        }
    },
    {
        id: 'etl',
        name: 'vltrn-etl',
        category: 'Data',
        status: 'ready',
        language: 'Python',
        price: 499,
        description: 'Complete ETL framework with 15+ built-in components, parallel processing, and extensible architecture. Transform data from any source to any destination.',
        examples: [
            {
                title: 'CSV to Database Pipeline',
                description: 'Extract from CSV, transform with filters and column additions, load to PostgreSQL in minutes.'
            },
            {
                title: 'API to Data Warehouse',
                description: 'Pull from REST APIs, normalize JSON, type cast fields, and load to Snowflake with parallel processing.'
            }
        ],
        features: [
            '15+ components',
            'Parallel processing',
            'Extensible architecture',
            '12 test cases'
        ]
    },
    {
        id: 'erc20-por',
        name: '@vltrn/erc20-por-template',
        category: 'Blockchain',
        status: 'ready',
        language: 'Solidity',
        price: 799,
        description: 'Production-ready ERC-20 token with Chainlink Proof of Reserves, role-based access, and pausable functionality. Includes 50+ tests.',
        examples: [
            {
                title: 'Deploy with Proof of Reserves',
                description: 'Deploy ERC-20 token integrated with Chainlink PoR for transparent collateral backing.'
            },
            {
                title: 'Role-Based Minting',
                description: 'Implement secure minting with role-based access control and emergency pause functionality.'
            }
        ],
        features: [
            'Chainlink PoR integration',
            'Role-based access',
            'Pausable functionality',
            '50+ test cases'
        ]
    },
    {
        id: 'lexicon-sdk',
        name: 'lexicon-sdk',
        category: 'Governance',
        status: 'ready',
        language: 'Python',
        price: 599,
        description: 'Institutional-grade knowledge governance with 14 domains, 55+ AI agents, Oracle consensus, and tamper-evident audit trails.',
        examples: [
            {
                title: 'Multi-Agent Orchestration',
                description: 'Detect teams of agents based on file context and chain them for complex tasks.'
            },
            {
                title: 'Oracle Governance',
                description: 'Propose decisions requiring multi-signature approval with configurable thresholds.'
            }
        ],
        features: [
            '14 knowledge domains',
            '55+ AI agents',
            'Oracle consensus',
            'Audit trails'
        ]
    },
    {
        id: 'council-smpc',
        name: 'council-smpc-sdk',
        category: 'Governance',
        status: 'ready',
        language: 'Python',
        price: 399,
        description: 'NVIDIA integration SDK with guardrails, capability routing, and identity templates for 462-agent system with GPU acceleration.',
        examples: [
            {
                title: 'NVIDIA-Accelerated Task',
                description: 'Route optimization tasks to NVIDIA cuOpt backend for GPU-powered route planning.'
            },
            {
                title: 'Agent Identity Generation',
                description: 'Generate complete identity files for new agents with tier and clearance specifications.'
            }
        ],
        features: [
            'NVIDIA routing',
            'Guardrails policy',
            'Identity templates',
            'CLI tools'
        ]
    },
    {
        id: 'carbon-sdk',
        name: '@carbon6/sdk',
        category: 'Collaboration',
        status: 'ready',
        language: 'Node.js',
        price: 199,
        description: 'Auto-commit collaboration SDK for creator platform. Automatic git sync, file watching, and tier-based revenue splits.',
        examples: [
            {
                title: 'Auto-Sync Workflow',
                description: 'Automatically commit and sync file changes with customizable commit message templates.'
            },
            {
                title: 'Team Coordination',
                description: 'View team activity, sync status, and coordinate work across Carbon Collective tiers.'
            }
        ],
        features: [
            'Auto-commit',
            'File watching',
            'Team coordination',
            'Tier management'
        ]
    },
    {
        id: 'vectordb',
        name: 'vltrn-vectordb',
        category: 'Data',
        status: 'dev',
        language: 'Python',
        price: 399,
        description: 'Vector database integration supporting Milvus, Qdrant, and Pinecone. Includes embedding generation and similarity search for AI applications.',
        examples: [
            {
                title: 'Semantic Search',
                description: 'Store documents with embeddings and perform semantic similarity search across your knowledge base.'
            },
            {
                title: 'Multi-Modal Embeddings',
                description: 'Search across images and text with multi-modal embeddings for visual search applications.'
            }
        ],
        features: [
            'Multi-provider support',
            'Embedding generation',
            'Similarity search',
            'Metadata filtering'
        ],
        completion: '40%'
    },
    {
        id: 'social-automation',
        name: '@vltrn/social-automation',
        category: 'Automation',
        status: 'dev',
        language: 'Node.js',
        price: 399,
        description: 'Social media automation pipeline for Twitter, Instagram, and LinkedIn. Schedule posts, auto-engage, and track analytics.',
        examples: [
            {
                title: 'Cross-Platform Scheduling',
                description: 'Schedule posts to multiple social platforms with images and optimal timing.'
            },
            {
                title: 'Auto-Engagement',
                description: 'Automatically like, comment, and engage with content matching specific hashtags or criteria.'
            }
        ],
        features: [
            'Multi-platform support',
            'Post scheduling',
            'Auto-engagement',
            'Analytics tracking'
        ],
        completion: '30%'
    },
    {
        id: 'content-scheduler',
        name: '@vltrn/content-scheduler',
        category: 'Automation',
        status: 'dev',
        language: 'Node.js',
        price: 299,
        description: 'Cron-based content scheduler with Bull queues and Redis. Schedule posts, emails, and tasks with timezone support.',
        examples: [
            {
                title: 'Recurring Blog Posts',
                description: 'Automatically publish blog posts on a recurring schedule with timezone awareness.'
            },
            {
                title: 'Drip Email Campaign',
                description: 'Create multi-day email sequences that trigger based on user actions or time delays.'
            }
        ],
        features: [
            'Cron scheduling',
            'Bull queues',
            'Timezone support',
            'Recurring patterns'
        ],
        completion: '30%'
    },
    {
        id: 'erc4626-vault',
        name: '@vltrn/erc4626-vault-template',
        category: 'Blockchain',
        status: 'dev',
        language: 'Solidity',
        price: 999,
        description: 'ERC-4626 tokenized vault for staking with emission schedule, reward distribution, and governance.',
        examples: [
            {
                title: 'Staking Vault',
                description: 'Deploy a staking vault where users deposit tokens and receive yield-bearing shares.'
            },
            {
                title: 'Reward Distribution',
                description: 'Automatically distribute rewards to stakers based on emission schedule and holding duration.'
            }
        ],
        features: [
            'ERC-4626 standard',
            'Emission schedule',
            'Reward distribution',
            'Governance ready'
        ],
        completion: '75%'
    },
    {
        id: 'docker-patterns',
        name: 'docker-patterns',
        category: 'Deployment',
        status: 'dev',
        language: 'Bash/YAML',
        price: 199,
        description: 'Production-ready Docker patterns for single-service, microservices, database integration, and production deployments.',
        examples: [
            {
                title: 'Microservices Stack',
                description: 'Deploy complete microservices architecture with API, workers, database, and Redis.'
            },
            {
                title: 'Production with Load Balancing',
                description: 'Production-grade deployment with multiple replicas, health checks, and zero-downtime updates.'
            }
        ],
        features: [
            'Multiple patterns',
            'Health checks',
            'Load balancing',
            'Production-ready'
        ],
        completion: '10%'
    },
    {
        id: 'health-checks',
        name: '@vltrn/health-checks',
        category: 'Deployment',
        status: 'dev',
        language: 'Node.js/Python',
        price: 149,
        description: 'Health check endpoints for Express and Flask with Kubernetes probes, dependency checks, and graceful shutdown.',
        examples: [
            {
                title: 'Express Health Endpoint',
                description: 'Add /health endpoint that checks database, Redis, and external service connectivity.'
            },
            {
                title: 'Kubernetes Probes',
                description: 'Configure liveness and readiness probes for zero-downtime Kubernetes deployments.'
            }
        ],
        features: [
            'Multi-framework',
            'Dependency checks',
            'K8s probes',
            'Graceful shutdown'
        ],
        completion: '10%'
    },
    {
        id: 'config-manager',
        name: 'vltrn-config',
        category: 'Utilities',
        status: 'dev',
        language: 'Python',
        price: 149,
        description: 'Configuration management with YAML/JSON/TOML support, environment overrides, schema validation, and hot reloading.',
        examples: [
            {
                title: 'Multi-Environment Config',
                description: 'Load different configurations for development, staging, and production environments.'
            },
            {
                title: 'Environment Overrides',
                description: 'Override any configuration value via environment variables for containerized deployments.'
            }
        ],
        features: [
            'Multi-format support',
            'Environment overrides',
            'Schema validation',
            'Hot reloading'
        ],
        completion: '10%'
    },
    {
        id: 'logging',
        name: '@vltrn/logging-systems',
        category: 'Utilities',
        status: 'dev',
        language: 'Python/Node.js',
        price: 149,
        description: 'Structured logging with JSON output, log aggregation, and integration with Datadog, Sentry, and CloudWatch.',
        examples: [
            {
                title: 'Structured Logging',
                description: 'Log events with structured data for easy filtering and analysis in log aggregation systems.'
            },
            {
                title: 'Request Tracing',
                description: 'Automatically add trace IDs to all logs for request correlation across microservices.'
            }
        ],
        features: [
            'Structured logging',
            'JSON output',
            'Request tracing',
            'Multiple integrations'
        ],
        completion: '0%'
    }
];

// Category metadata
const CATEGORIES = {
    'Trading': { color: '#10b981', count: 3 },
    'Auth': { color: '#8b5cf6', count: 2 },
    'Infrastructure': { color: '#6366f1', count: 3 },
    'APIs': { color: '#06b6d4', count: 3 },
    'Data': { color: '#f59e0b', count: 2 },
    'Automation': { color: '#ec4899', count: 2 },
    'Blockchain': { color: '#eab308', count: 2 },
    'Deployment': { color: '#3b82f6', count: 2 },
    'Utilities': { color: '#64748b', count: 2 },
    'Governance': { color: '#7c3aed', count: 2 },
    'Collaboration': { color: '#14b8a6', count: 1 }
};

// Export for use in tools.js
window.SDK_DATA = SDK_DATA;
window.CATEGORIES = CATEGORIES;
