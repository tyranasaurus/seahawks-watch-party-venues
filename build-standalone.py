import re, base64, subprocess, os, tempfile

SRC_HTML = "/Users/goblins/projects/abha-udit-wedding/index.html"
OUT_HTML = "/Users/goblins/projects/abha-udit-wedding/seahawks-watch-party-venues-standalone.html"
ROOT = "/Users/goblins/projects/abha-udit-wedding"
MAXDIM = 1200
QUALITY = "68"

html = open(SRC_HTML).read()
paths = sorted(set(re.findall(r'images/[A-Za-z0-9._-]+\.(?:jpg|jpeg|png|webp)', html)))
print(f"found {len(paths)} unique image references")

tmp = tempfile.mkdtemp()
raw_total = 0
opt_total = 0
for p in paths:
    src = os.path.join(ROOT, p)
    raw_total += os.path.getsize(src)
    out = os.path.join(tmp, os.path.basename(p) + ".jpg")
    dims = subprocess.check_output(["sips", "-g", "pixelWidth", "-g", "pixelHeight", src]).decode()
    w = int(re.search(r"pixelWidth: (\d+)", dims).group(1))
    h = int(re.search(r"pixelHeight: (\d+)", dims).group(1))
    args = ["sips", "-s", "format", "jpeg", "-s", "formatOptions", QUALITY]
    if max(w, h) > MAXDIM:
        args += ["-Z", str(MAXDIM)]
    args += [src, "--out", out]
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    data = open(out, "rb").read()
    opt_total += len(data)
    uri = "data:image/jpeg;base64," + base64.b64encode(data).decode()
    assert html.count(p) >= 1, f"path not found in html: {p}"
    html = html.replace(p, uri)

open(OUT_HTML, "w").write(html)
print(f"raw images:       {raw_total/1e6:.1f} MB")
print(f"optimized images: {opt_total/1e6:.1f} MB")
print(f"standalone html:  {os.path.getsize(OUT_HTML)/1e6:.1f} MB")
# sanity: no leftover relative image refs in the standalone
leftovers = re.findall(r'(?<!data:image/jpeg;base64,)images/[A-Za-z0-9._-]+\.(?:jpg|jpeg|png|webp)', html)
print(f"leftover relative image refs: {len(leftovers)}")
