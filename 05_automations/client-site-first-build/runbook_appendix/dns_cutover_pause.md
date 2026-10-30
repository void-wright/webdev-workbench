# Appendix: Pause Point #2: Nameserver Flip (site ports only)

> Public edition. Stop before the cutover. The build assistant never touches the registrar; the domain owner does this step by hand.

## When

After all preview redirect checks pass and the redirect archive is saved.

## What the build assistant prints (in its voice)

> *"Every redirect is live on the preview and curl-tested: <N> total, <H> high-priority, <A> assets placed and reachable, 100% pass on exact rules, <R> pattern rules checked by hand. Before the cutover, the domain's nameservers need to point at Cloudflare.*
> *1. In Cloudflare, the zone for <SITE_DOMAIN> shows two assigned nameservers. (I read them from the API; they are below.)*
> *2. At your registrar, open the domain's nameserver settings, choose custom nameservers, and enter exactly those two. Save.*
> *3. Before you switch: if the domain has DNSSEC enabled at the registrar, turn it off there first; after the move, enable DNSSEC in Cloudflare and add the new DS record at the registrar.*
> *4. Propagation can take up to 48 hours. Reply 'nameservers ready' when you have saved them."*

Read the two nameservers from the zone and print them; never type them from memory. Run this command from the package root:

```bash
bash 06_web_tools/cf-api GET '/zones?name=<SITE_DOMAIN>'   # result[0].name_servers and result[0].status
```

## Continuation signals

- **"nameservers ready"**: The build assistant reads the zone back (`status` = `active`) and checks a public resolver for the NS records. Only when both agree does it proceed with the cutover: build with production settings, attach the custom domain to the Worker, run the full redirect suite against the live domain, submit the sitemap again in Search Console, and mark the redirect manifest as verified on the live site in the site record.
- **"hold off"**: stay paused, indefinitely.

## Why it is a hard halt

A cutover with partially propagated nameservers can serve some visitors the old site and others the new one. A redirect check through one resolver cannot verify every visitor's route. The pause gives the domain owner control over when the switch begins and requires observable DNS checks before proceeding; it does not make global propagation instantaneous.
