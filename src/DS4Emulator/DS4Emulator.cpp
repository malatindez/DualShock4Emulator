
#define DS4EMULATOR_API extern "C" __declspec(dllexport)

#define WIN32_LEAN_AND_MEAN
#include <ViGEm/Client.h>
#include <Windows.h>

#include <chrono>
#include <iostream>
#include <thread>

//#define MUTEX_SAFETY

#ifdef MUTEX_SAFETY
#include <mutex>
#endif

#define __DEBUG_MESSAGES

#define EMULATOR_TICKRATE 1

struct DS4_CONTEXT {
  PVIGEM_CLIENT client;
  VIGEM_ERROR ret;
  PVIGEM_TARGET ds4;
  DS4_REPORT_EX report;
  bool thread_running = true;
  std::thread* thread;
} * context;

uint64_t GetCurrentTimeInMicroseconds() {
  using namespace std::chrono;
  auto now = time_point_cast<microseconds>(system_clock::now());
  return now.time_since_epoch().count();
}

VOID CALLBACK notification(PVIGEM_CLIENT, PVIGEM_TARGET, UCHAR, UCHAR,
                           DS4_LIGHTBAR_COLOR, LPVOID) {
  return;
}

void ClearReport() {
  DS4_REPORT_INIT_EX(&(context->report));
  context->report.bTouchPacketsN = 0;
  context->report.sCurrentTouch = {0};
  context->report.sPreviousTouch[0] = {0};
  context->report.sPreviousTouch[1] = {0};
  context->report.sCurrentTouch.bIsUpTrackingNum1 = 0x80;
  context->report.sCurrentTouch.bIsUpTrackingNum2 = 0x80;
}

void SendReport() {
  context->ret = vigem_target_ds4_update_ex(context->client, context->ds4,
                                            context->report);
}
// each variable is defined in microseconds.
struct Report {
  uint64_t up = 0, right = 0, down = 0, left = 0, triangle = 0, circle = 0,
           cross = 0, square = 0, l1 = 0, r1 = 0, thumb_left = 0,
           thumb_right = 0, options = 0, share = 0, touchpad = 0, l2 = 0,
           r2 = 0, move_left_thumb = 0, move_right_thumb = 0;
  int8_t l2_x = 0, r2_x = 0, left_thumb_x = 0, left_thumb_y = 0,
         right_thumb_x = 0, right_thumb_y = 0;
} * current_report;

#ifdef MUTEX_SAFETY
std::mutex report_mutex;
#endif

void FormReport() {
#ifdef MUTEX_SAFETY
  std::lock_guard<std::mutex> guard(report_mutex);
#endif
  uint64_t now = GetCurrentTimeInMicroseconds();

  if (current_report->up > now) {
    DS4_SET_DPAD_EX(&context->report, DS4_BUTTON_DPAD_NORTH);
  }
  if (current_report->right > now) {
    DS4_SET_DPAD_EX(&context->report, DS4_BUTTON_DPAD_EAST);
  }
  if (current_report->down > now) {
    DS4_SET_DPAD_EX(&context->report, DS4_BUTTON_DPAD_SOUTH);
  }
  if (current_report->left > now) {
    DS4_SET_DPAD_EX(&context->report, DS4_BUTTON_DPAD_WEST);
  }

  if (current_report->square > now) {
    context->report.wButtons |= DS4_BUTTON_SQUARE;
  }
  if (current_report->cross > now) {
    context->report.wButtons |= DS4_BUTTON_CROSS;
  }
  if (current_report->circle > now) {
    context->report.wButtons |= DS4_BUTTON_CIRCLE;
  }
  if (current_report->triangle > now) {
    context->report.wButtons |= DS4_BUTTON_TRIANGLE;
  }
  // L1
  if (current_report->l1 > now) {
    context->report.wButtons |= DS4_BUTTON_SHOULDER_LEFT;
  }
  // R1
  if (current_report->r1 > now) {
    context->report.wButtons |= DS4_BUTTON_SHOULDER_RIGHT;
  }
  // L2; degree should be equal to 255 to click
  if (current_report->l2 > now) {
    context->report.bTriggerL = current_report->l2_x;
    if (context->report.bTriggerL > 0)
      context->report.wButtons |= DS4_BUTTON_TRIGGER_LEFT;
  }
  // R2; degree should be equal to 255 to click
  if (current_report->r2 > now) {
    context->report.bTriggerR = current_report->r2_x;
    if (context->report.bTriggerR > 0)
      context->report.wButtons |= DS4_BUTTON_TRIGGER_RIGHT;
  }

  if (current_report->move_left_thumb > now) {
    context->report.bThumbLX =
        uint8_t(int16_t(current_report->left_thumb_x) + 128);
    context->report.bThumbLY =
        uint8_t(int16_t(current_report->left_thumb_y) + 128);
  }
  if (current_report->move_right_thumb > now) {
    context->report.bThumbRX =
        uint8_t(int16_t(current_report->right_thumb_x) + 128);
    context->report.bThumbRY =
        uint8_t(int16_t(current_report->right_thumb_y) + 128);
  }

  if (current_report->options > now) {
    context->report.wButtons |= DS4_BUTTON_OPTIONS;
  }
  if (current_report->share > now) {
    context->report.wButtons |= DS4_BUTTON_SHARE;
  }
  if (current_report->touchpad > now) {
    context->report.bSpecial |= DS4_SPECIAL_BUTTON_TOUCHPAD;
  }

  if (current_report->thumb_left > now) {
    context->report.wButtons |= DS4_BUTTON_THUMB_LEFT;
  }
  if (current_report->thumb_right > now) {
    context->report.wButtons |= DS4_BUTTON_THUMB_RIGHT;
  }
}

void main_emulator_thread() {
  while (context->thread_running) {
    ClearReport();
    FormReport();
    SendReport();
    Sleep(EMULATOR_TICKRATE);
  }
}

bool DS4Init() {
  context = new DS4_CONTEXT;
  current_report = new Report;
  context->client = vigem_alloc();
  context->ret = vigem_connect(context->client);
  std::cout << context->ret << std::endl;
  context->ds4 = vigem_target_ds4_alloc();
  auto client = context->client;
  auto ds4 = context->ds4;
  context->ret = vigem_target_add(client, ds4);
  std::cout << context->ret << std::endl;
  context->ret = vigem_target_ds4_register_notification(client, ds4,
                                                        &notification, nullptr);
  std::cout << context->ret << std::endl;
  context->thread = new std::thread(main_emulator_thread);
  return true;
}

void DS4Unload() {
  std::cout << "Unloading DS4..." << std::endl;
  vigem_target_remove(context->client, context->ds4);
  vigem_target_free(context->ds4);
  vigem_free(context->client);
  context = nullptr;
}

DS4EMULATOR_API void ShowContext() { std::cout << context; }

DS4EMULATOR_API void HoldUp(uint64_t microsec) {
#ifdef MUTEX_SAFETY
  std::lock_guard<std::mutex> guard(report_mutex);
#endif
#ifdef __DEBUG_MESSAGES
  std::cout << microsec << std::endl;
#endif
  current_report->up = microsec;
}
DS4EMULATOR_API void HoldRight(uint64_t microsec) {
#ifdef MUTEX_SAFETY
  std::lock_guard<std::mutex> guard(report_mutex);
#endif
#ifdef __DEBUG_MESSAGES
  std::cout << microsec << std::endl;
#endif
  current_report->right = microsec;
}
DS4EMULATOR_API void HoldDown(uint64_t microsec) {
#ifdef MUTEX_SAFETY
  std::lock_guard<std::mutex> guard(report_mutex);
#endif
#ifdef __DEBUG_MESSAGES
  std::cout << microsec << std::endl;
#endif
  current_report->down = microsec;
}
DS4EMULATOR_API void HoldLeft(uint64_t microsec) {
#ifdef MUTEX_SAFETY
  std::lock_guard<std::mutex> guard(report_mutex);
#endif
#ifdef __DEBUG_MESSAGES
  std::cout << microsec << std::endl;
#endif
  current_report->left = microsec;
}

DS4EMULATOR_API void HoldTriangle(uint64_t microsec) {
#ifdef MUTEX_SAFETY
  std::lock_guard<std::mutex> guard(report_mutex);
#endif
#ifdef __DEBUG_MESSAGES
  std::cout << microsec << std::endl;
#endif
  current_report->triangle = microsec;
}
DS4EMULATOR_API void HoldCircle(uint64_t microsec) {
#ifdef MUTEX_SAFETY
  std::lock_guard<std::mutex> guard(report_mutex);
#endif
#ifdef __DEBUG_MESSAGES
  std::cout << microsec << std::endl;
#endif
  current_report->circle = microsec;
}
DS4EMULATOR_API void HoldCross(uint64_t microsec) {
#ifdef MUTEX_SAFETY
  std::lock_guard<std::mutex> guard(report_mutex);
#endif
#ifdef __DEBUG_MESSAGES
  std::cout << microsec << std::endl;
#endif
  current_report->cross = microsec;
}
DS4EMULATOR_API void HoldSquare(uint64_t microsec) {
#ifdef MUTEX_SAFETY
  std::lock_guard<std::mutex> guard(report_mutex);
#endif
#ifdef __DEBUG_MESSAGES
  std::cout << microsec << std::endl;
#endif
  current_report->square = microsec;
}

DS4EMULATOR_API void HoldLeftShoulder(uint64_t microsec) {
#ifdef MUTEX_SAFETY
  std::lock_guard<std::mutex> guard(report_mutex);
#endif
#ifdef __DEBUG_MESSAGES
  std::cout << microsec << std::endl;
#endif
  current_report->l1 = microsec;
}

DS4EMULATOR_API void HoldRightShoulder(uint64_t microsec) {
#ifdef MUTEX_SAFETY
  std::lock_guard<std::mutex> guard(report_mutex);
#endif
#ifdef __DEBUG_MESSAGES
  std::cout << microsec << std::endl;
#endif
  current_report->r1 = microsec;
}

// L2; degree should be equal to 255 to click
DS4EMULATOR_API void LeftTrigger(uint64_t microsec, uint8_t degree) {
#ifdef MUTEX_SAFETY
  std::lock_guard<std::mutex> guard(report_mutex);
#endif
#ifdef __DEBUG_MESSAGES
  std::cout << microsec << std::endl;
#endif
  current_report->l2 = microsec;
  current_report->l2_x = degree;
}
// R2; degree should be equal to 255 to click
DS4EMULATOR_API void RightTrigger(uint64_t microsec, uint8_t degree) {
#ifdef MUTEX_SAFETY
  std::lock_guard<std::mutex> guard(report_mutex);
#endif
#ifdef __DEBUG_MESSAGES
  std::cout << microsec << std::endl;
#endif
  current_report->r2 = microsec;
  current_report->r2_x = degree;
}

DS4EMULATOR_API void MoveLeftThumb(uint64_t microsec, int8_t x, int8_t y) {
#ifdef MUTEX_SAFETY
  std::lock_guard<std::mutex> guard(report_mutex);
#endif
#ifdef __DEBUG_MESSAGES
  std::cout << microsec << std::endl;
#endif
  current_report->move_left_thumb = microsec;
  current_report->left_thumb_x = x;
  current_report->left_thumb_y = y;
}
DS4EMULATOR_API void MoveRightThumb(uint64_t microsec, int8_t x, int8_t y) {
#ifdef MUTEX_SAFETY
  std::lock_guard<std::mutex> guard(report_mutex);
#endif
#ifdef __DEBUG_MESSAGES
  std::cout << microsec << std::endl;
#endif
  current_report->move_right_thumb = microsec;
  current_report->right_thumb_x = x;
  current_report->right_thumb_y = y;
}

DS4EMULATOR_API void HoldOptions(uint64_t microsec) {
#ifdef MUTEX_SAFETY
  std::lock_guard<std::mutex> guard(report_mutex);
#endif
#ifdef __DEBUG_MESSAGES
  std::cout << microsec << std::endl;
#endif
  current_report->options = microsec;
}
DS4EMULATOR_API void HoldShare(uint64_t microsec) {
#ifdef MUTEX_SAFETY
  std::lock_guard<std::mutex> guard(report_mutex);
#endif
#ifdef __DEBUG_MESSAGES
  std::cout << microsec << std::endl;
#endif
  current_report->share = microsec;
}
DS4EMULATOR_API void HoldTouchpad(uint64_t microsec) {
#ifdef MUTEX_SAFETY
  std::lock_guard<std::mutex> guard(report_mutex);
#endif
#ifdef __DEBUG_MESSAGES
  std::cout << microsec << std::endl;
#endif
  current_report->touchpad = microsec;
}

DS4EMULATOR_API void HoldLeftThumb(uint64_t microsec) {
#ifdef MUTEX_SAFETY
  std::lock_guard<std::mutex> guard(report_mutex);
#endif
#ifdef __DEBUG_MESSAGES
  std::cout << microsec << std::endl;
#endif
  current_report->thumb_left = microsec;
}
DS4EMULATOR_API void HoldRightThumb(uint64_t microsec) {
#ifdef MUTEX_SAFETY
  std::lock_guard<std::mutex> guard(report_mutex);
#endif
#ifdef __DEBUG_MESSAGES
  std::cout << microsec << std::endl;
#endif
  current_report->thumb_right = microsec;
}

bool CreateRegistryKey(HKEY hKeyRoot, LPCTSTR pszSubKey) {
  HKEY hKey;
  DWORD dwFunc;
  LONG lRet;
  //------------------------------------------------------------------------------
  SECURITY_DESCRIPTOR SD;
  SECURITY_ATTRIBUTES SA;
  if (!InitializeSecurityDescriptor(&SD, SECURITY_DESCRIPTOR_REVISION))
    return false;
  if (!SetSecurityDescriptorDacl(&SD, true, 0, false)) return false;
  SA.nLength = sizeof(SA);
  SA.lpSecurityDescriptor = &SD;
  SA.bInheritHandle = false;
  //------------------------------------------------------------------------------
  lRet =
      RegCreateKeyEx(hKeyRoot, pszSubKey, 0, (LPTSTR)NULL,
                     REG_OPTION_NON_VOLATILE, KEY_WRITE, &SA, &hKey, &dwFunc);
  if (lRet == ERROR_SUCCESS) {
    RegCloseKey(hKey);
    hKey = (HKEY)NULL;
    return true;
  }
  SetLastError((DWORD)lRet);
  return false;
}

BOOL FileExists(LPCWSTR szPath) {
  DWORD dwAttrib = GetFileAttributesW(szPath);
  return (dwAttrib != INVALID_FILE_ATTRIBUTES &&
          !(dwAttrib & FILE_ATTRIBUTE_DIRECTORY));
}
bool DirExists(LPCWSTR szPath) {
  DWORD dwAttrib = GetFileAttributesW(szPath);
  return (dwAttrib != INVALID_FILE_ATTRIBUTES &&
          (dwAttrib & FILE_ATTRIBUTE_DIRECTORY));
}

std::wstring GetEnv(std::wstring var) {
  DWORD bufferSize = 65535;
  std::wstring buff;
  buff.resize(bufferSize);
  bufferSize = GetEnvironmentVariableW(var.c_str(), &buff[0], bufferSize);
  buff.resize(bufferSize);
  return buff;
}
std::wstring GetPathToFile() {
  std::wstring file_path = GetEnv(L"APPDATA") + L"\\DS4Emulator";
  if (!DirExists(file_path.c_str())) {
    CreateDirectoryW(file_path.c_str(), NULL);
  }
  file_path += L"\\latest_handle";
  HANDLE file = CreateFileW(file_path.c_str(), GENERIC_READ | GENERIC_WRITE, 0,
                            NULL, CREATE_NEW, FILE_ATTRIBUTE_NORMAL, NULL);
  CloseHandle(file);
  return file_path;
}

bool CheckIfDLLIsSingle() {
  std::wstring file_path = GetPathToFile();

  HANDLE file = CreateFileW(file_path.c_str(), GENERIC_READ, 0, NULL,
                            OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);

  HMODULE handle_in_file = NULL;
  DWORD lpRead;
  if (!ReadFile(file, &handle_in_file, sizeof(HMODULE), &lpRead, NULL) ||
      lpRead != sizeof(HMODULE)) {
    handle_in_file = NULL;
  }
  CloseHandle(file);

  HMODULE handle = GetModuleHandleA(NULL);

  if (handle_in_file == handle) {
    return false;
  }

  file = CreateFileW(file_path.c_str(), GENERIC_WRITE, 0, NULL, CREATE_ALWAYS,
                     FILE_ATTRIBUTE_NORMAL, NULL);

  WriteFile(file, &handle, sizeof(HMODULE), &lpRead, NULL);

  CloseHandle(file);

  return true;
}
void ClearHandleFile() {
  std::wstring file_path = GetPathToFile();
  HANDLE file = CreateFileW(file_path.c_str(), GENERIC_WRITE, 0, NULL,
                            CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
  CloseHandle(file);
}
BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call,
                      LPVOID lpReserved) {
  bool temp = true;
  switch (ul_reason_for_call) {
    case DLL_PROCESS_ATTACH:
      temp = CheckIfDLLIsSingle();
      if (!temp) {
        std::cout << "DLL is already loaded somewhere.\nYou can not use it "
                     "more than once.\n";
        return false;
      }
      DS4Init();
      break;
    case DLL_THREAD_ATTACH:
      break;
    case DLL_THREAD_DETACH:
      break;
    case DLL_PROCESS_DETACH:
      context->thread_running = false;
      DS4Unload();
      ClearHandleFile();
      break;
  }
  return TRUE;
}