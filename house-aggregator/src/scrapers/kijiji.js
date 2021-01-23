const axios = require('axios');
const cheerio = require('cheerio');
const { exception } = require('console');
const fs = require("fs");

module.exports = {
    name: "Kijiji.ca",
    baseURL: "https://www.kijiji.ca",
    search: "/b-kingston-on/student-housing/k0l1700183",
    cleanupText(s) {

        return s.replace(/(\r\n|\n|\r|)/gm, "").trim();
    },
    async execute() {
        
        await new Promise(resolve => setTimeout(resolve, 5000));
        return await this.getResults(this.search, [], 1);
    },
    async getResults(search, results, depth) {

        console.log(`Getting results for page ${depth}`);

        let html;
        let $;

        try {
            html = await axios.get(this.baseURL + search);

            if (html === undefined) throw new exception("fuck everything")

            $ = cheerio.load(html.data);
        }
        catch (err) {
            console.error(err.message);
        }

        let urls = $("#mainPageContent > div.layout-3 > div.col-2 > div:nth-child(3)").children("div.search-item").map((_, el) => {
            return $(el).attr("data-vip-url");
        }).get();

        const posts = await Promise.all(urls.map(s => axios.get(this.baseURL + s)));

        console.log(`Got ${posts.length} results.`);

        $("#mainPageContent > div.layout-3 > div.col-2 > div:nth-child(3)").children("div.search-item").each((i, wrapperEl) => {

            const entry = {};
            const $$ = cheerio.load(posts[i].data);

            $(wrapperEl).children("div.clearfix").children(".info").children().children().each((_, el) => {

                let className = this.cleanupText($(el).attr("class"));

                if (className == "location") {

                    entry["date-posted"] = this.cleanupText($(el).children("span.date-posted").text());
                }

                else if (className == "description") {
                    return true;
                }

                else {
                    entry[className] = $(el).text().replace(/(\r\n|\n|\r|)/gm, "").trim();
                }
            });

            entry["description"] = $$("#vip-body > div.root-2377010271.light-3420168793.card-745541139 > div > div.showMoreChild-3420331552.showMoreChild__newRentals-917604537 > div").first().text();
            entry["address"] = $$("span[itemprop='address']").text();
            entry["landlord"] = $$("#vip-body > div.itemInfoSidebar-408428561.itemInfoSidebar__newRentals-3379548915 > div.r2s-1114502950 > h3 > span").text();
            entry["bedrooms"] = $$("#vip-body > div.realEstateTitle-1440881021 > div.unitRow-1281171205 > div > li:nth-child(2) > span").text();

            results.push(entry);
        });

        let next = $('#mainPageContent > div.layout-3 > div.col-2 > div:nth-child(3) > div.bottom-bar > div.pagination > a').filter((_, el) => {

            return $(el).attr("href").match(new RegExp(`/page-${depth + 1}/`, "g")) != null;
        }).first().attr("href");

        if (next != null || next != undefined) {
            results = this.getResults(next, results, ++depth);
        };

        return results;
    }
}