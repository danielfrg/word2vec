#if !defined WIN32_LEAN_AND_MEAN
# define WIN32_LEAN_AND_MEAN
#endif
#include <windows.h>
#include <process.h>
#include <assert.h>

typedef struct {
  void * (*pthread_routine)(void *);
  void * pthread_arg;
  HANDLE handle;
} pthread_t;

static unsigned __stdcall win32_start_routine(void * arg) {
  pthread_t * p = (pthread_t *)arg;
  p->pthread_routine(p->pthread_arg);
  return 0;
}

static int pthread_create(pthread_t * id,
                          void * attr,
                          void * (*start_routine)(void *),
                          void * arg)
{
  assert(attr == 0);
  id->pthread_routine = start_routine;
  id->pthread_arg = arg;
  id->handle = (HANDLE)_beginthreadex(0, 0, win32_start_routine, (void *)id, 0, 0);
  if (id->handle != 0)
    return 0;
  return -1;
}

static int pthread_join(pthread_t thread, void ** retval) {
  WaitForSingleObject(thread.handle, INFINITE);
  if (retval) {
    *retval = 0;
  }
  return 0;
}

static void pthread_exit(void * p) {
  _endthreadex(0);
}

static int posix_memalign(void ** memptr, size_t alignment, size_t size) {
  assert(memptr);
  *memptr = _aligned_malloc(size, alignment);
  if (*memptr) {
    return 0;
  } else {
    return -1;
  }
}
