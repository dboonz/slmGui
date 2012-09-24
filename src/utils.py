
def w2f(wavelength):
  " wavelength [nm] to frequency [Hz] conversion"
  return 299792458./wavelength*1e9

def f2w(frequency):
  " frequency [Hz] to wavelength [nm] conversion"
  return 299792458./frequency*1e9

if __name__ == '__main__':
  print "Testing: wl 2 f 2 wl @ 780 nm"
  print w2f(f2w(780))

