import logging
import time

logger = logging.getLogger(__name__)

def time_fn(fn):

    def wrapper(*args, **kwargs):

        start = time.time()


        res = fn(*args, **kwargs)

        logger.info(f"Function: {fn.__name__}({','.join(map(str,args))}, {','.join(map(lambda i: f'{i[0]}={i[1]}', kwargs.items()))}) "
                    f"finished after: {time.time() - start:.6f} seconds")
        # logger.info(f"Returning: {res}")

        return res

    return wrapper