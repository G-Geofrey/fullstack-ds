# Logging in Python
## Notes 
- Root logger is the highest level logger.
    - It is created with levele WARNING
    - By default has `StreamHandler` that outputs to `sys.stderr`
- Even when using named loggers, it is good to configure the root logger using `logging.basicConfig()`
- When a logger is created, the level is set to NOTSET. If a logger has a level of NOTSET, its chain of ancestor loggers is traversed until either an ancestor with a level other than NOTSET is found, or the root is reached.
- When a logger is called e.g `logger.info(...)`, the logger first checks if it has any handlers, if no handlers are found, the logger traverses its ancestor loggers unitl it reaches one with handlers or reaches the root logger.
- Loggers should never be instantiated directly but always through the module-level function `logging.geLogger(name)`.
- Low level (child) loggers forward messages to higher-level (parents/ancestors).
    - This approach is known as hierarchical logging.
    - Messages are forwarded to higher level loggers only if the logging level and filters at the child logger are satisfied.
    - Can be disabled by setting the `propagate` property of the logger to false e.g `logger.propagate=False`.