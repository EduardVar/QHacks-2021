const axios = require('axios');
const cheerio = require('cheerio');
const fs = require("fs");

module.exports = {
    name: "Kijiji.ca",
    baseURL: "https://www.kijiji.ca",
    search: "/b-kingston-on/student-housing/k0l1700183",
    cleanupText(s) {

        return s.replace(/(\r\n|\n|\r|)/gm, "").trim();
    },
    async execute() {

        let page = 1;
        let done = false;

        const results = []
        let s = this.search;
        let i = 0;

        while (!done) {

            let html = await axios.get(this.baseURL + s);
            let $ = cheerio.load(html.data);

            $("#mainPageContent > div.layout-3 > div.col-2 > div:nth-child(3)").children("div.search-item").each((_, y) => {

                results.push({});

                $(y).children("div.clearfix").children(".info").children().children().each((_, el) => {

                    let text = $(el).text().replace(/(\r\n|\n|\r|)/gm, "").trim();
                    let className = this.cleanupText($(el).attr("class"));

                    if (className == "location") {

                        results[i] = {
                            ...results[i], ...{
                                "date-posted": this.cleanupText($(el).children("span.date-posted").text()),
                                "location": this.cleanupText($(el).children().first().text()),
                            }
                        };
                    }

                    else {
                        results[i] = { ...results[i], [className]: text };
                    }
                });

                i++;
            });

            let isNextPage = $('#mainPageContent > div.layout-3 > div.col-2 > div:nth-child(3) > div.bottom-bar > div.pagination > a').filter((i, el) => {

                return $(el).attr("href").match(new RegExp(`/page-${page + 1}/`, "g")) != null;
            });

            let newSearch = isNextPage.first().attr("href");

            done = newSearch == null || newSearch == undefined;
            if (!done) {
                console.log(`Done on page ${page}, moving onto next page.`);
                s = newSearch;
            }
            else (console.log(`Finished scraping on page ${page}`));
            page++;
        }

        return results
    }
}

module.exports.execute().then(res => {
    console.log(res);
    console.log(`Got ${res.length} results`);
    fs.writeFileSync("output.json", JSON.stringify(res));
}).catch(err => {
    let d = new Date();
    let name = `error-${d.getTime()}.txt`;
    fs.writeFileSync(name, err);
    console.error(err);
    console.error(`Got an error and wrote to ${name}`)
});