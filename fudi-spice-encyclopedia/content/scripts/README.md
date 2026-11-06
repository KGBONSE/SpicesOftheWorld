# Scripts to import

Drop your `.md` / `.txt` scripts here, then run `npm run import:scripts`.

Your scripts currently live in `../spicesOftheWorld/scripts/` in this repo, so you can skip copying and run:

```
npm run import:scripts -- --dry-run --dir ../spicesOftheWorld/scripts
npm run import:scripts -- --dir ../spicesOftheWorld/scripts
```

By default the `*-filming-script.md` and `*-read-aloud.md` production files are skipped (34 main episode scripts are imported). Add `--include-all` to import those as well.
