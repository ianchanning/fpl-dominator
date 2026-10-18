# RFC-012: Pipeline to ingest gameweek data

These are the CSS paths of the tables that we ingest for `bamf rip`:

### Gameweek data for `bamf rip [gkp|def|mid|fwd|squad]`

https://fantasy.premierleague.com/en/transfers

- must log-in

- select dropdown select at `html.light-theme body.is-logged-out main#mainContent.ism div#root div._1ksll754x div.ism div.eu9oece div.eu9oec1.eu9oec0 section div.eu9oec5 div.jw51ht0 div._1nvnlp40 div._1nvnlp42 div.enaqz30 div.react-aria-Select button#react-aria7861781041-_r_2if_._1gkly0o2._1gkly0o1._1gkly0o0._1gkly0o3`

- Copy the Outer HTML for, Goalkeepers/Defenders/Midfielders/Forwards, CSS Path for the `<table>`: `html.light-theme body.is-logged-out main#mainContent.ism div#root div._1ksll754x div.ism div.eu9oece div.eu9oec1.eu9oec0 section div.eu9oec5 div.jw51ht0 div._1nvnlp40 div._1nvnlp49 table._1nvnlp41`

- select radio button for Squad 'list' at `html.light-theme body.is-logged-out main#mainContent.ism div#root div._1ksll754x div.ism div.eu9oece div.eu9oec1.eu9oec0 div.eu9oec4 section div.jw51ht0 div.eu9oec3 div._187da710 div._187da711 div._1zmuz70 button.ktbkv41.ktbkv40._4xqwov0`

- Copy Outer HTML for Squad: `html.light-theme body.is-logged-out main#mainContent.ism div#root div._1ksll754x div.ism div.eu9oece div.eu9oec1.eu9oec0 div.eu9oec4 section div.jw51ht0 div.eu9oec3 div._4xqwov7 table._4xqwov8`

### Gameweek data for `bamf rip [fix|fix-a|fix-d]`

https://members.fantasyfootballscout.co.uk/season-ticker/

- must log-in

- select dropdown at `html.wf-francoisoneregular-n4-inactive.wf-inactive body.page.js div.antialiased.bg-gray-50.dark:bg-gray-900 main.p-4.md:ml-64.h-auto.pt-20 div.section div#fpl-ticker-root div.fpl-ticker-app div.advanced-ticker div div.ticker-controls div.control-group select.control-select`

- Copy the Outer HTML for Overall, Attack, Defence: `html.wf-francoisoneregular-n4-inactive.wf-inactive body.page.js div.antialiased.bg-gray-50.dark:bg-gray-900 main.p-4.md:ml-64.h-auto.pt-20 div.section div#fpl-ticker-root div.fpl-ticker-app div.advanced-ticker`
