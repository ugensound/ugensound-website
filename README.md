# Ugen Sound website

Static HTML/CSS portfolio for **https://www.ugensound.com**.

## Important: restore missing media before publication

The source ZIP did not include the original `media/` folder. Copy **all of its contents** into `media/` before deploying. At least these files are referenced in the HTML:

- `media/vi.jpg`
- `media/ale.png`
- `media/fla.png`
- `media/sdvi.jpg`
- `media/flmk.jpg`
- `media/ppal.jpg`

Check all assets and sizes with:

```bash
python3 tools/check_site.py
```

No PHP runtime or build system is needed. The legacy diagnostic PHP file and backup have not been included.

## Deploy on GitHub Pages

1. Create a **public** repository, e.g. `ugen-website`, on the GitHub account that will own the website.
2. Place **the contents** of this folder (not the outer folder itself) in the root of the repository, with the completed `media/` directory.
3. Open **Settings → Pages → Build and deployment** and select **Deploy from a branch**, `main`, `/(root)`; save.
4. **First test** the deployment at `https://<YOUR-GITHUB-ACCOUNT>.github.io/ugen-website/` (replace account/repository). No `CNAME` file is included yet, so the GitHub Pages preview works without redirecting to the domain.
5. Under **Settings → Pages → Custom domain**, set `www.ugensound.com` and save. GitHub automatically creates `CNAME` when publishing from a branch.
6. Only after GitHub recognizes the custom domain, update Aruba DNS: `www` CNAME → `<YOUR-GITHUB-ACCOUNT>.github.io` (replace account; omit repository path).
7. To route `ugensound.com` to the `www` site too, set the four GitHub Pages apex `A` records on Aruba (listed below) and remove conflicting old `A`/`AAAA` records only after checking their purpose.
8. Wait for GitHub certificate provisioning and enable **Enforce HTTPS**.

Root domain A records (`@`):

```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

**Do not delete Google mail MX/TXT/DKIM/SPF/DMARC records**. Keep any domain verification records as well.

Official documentation: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site

## Publishing / storage considerations

- GitHub Pages has a **1 GB published-site size limit** and **100 GB/month soft bandwidth limit**. Check the complete `media` folder size before publishing.
- Normal Git pushes reject individual Git files larger than **100 MiB**; GitHub's browser upload is more restrictive. Use local `git` for sizable assets, but keep individual files below the supported limit.
- If updates to binary media are frequent, optimize them first; history stores previous versions.
- This site currently uses CDN UIkit / fonts / Animate.css, an externally hosted CSS background image, embedded YouTube media, and Iubenda policy links. No dependency bundling has been done.
- `faq.html` is still a *page under construction*, as in the original site.

## Local preview

```bash
python3 -m http.server 8000
# open http://localhost:8000
```
