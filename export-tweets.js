#!/usr/bin/env node

const fs = require('fs');

const fileName = 'tweet.js';
const pathPrefix = './converted_tweets';

const chronTweets = (a, b) => (new Date(a.created_at)) - (new Date(b.created_at));

const humanize = (n) => {
  const x = n;
  return (x < 10 ? "0" : "" ) + x;
}

const presenter = (t) => {
  const p = {};
  const keys = 'id_str,created_at,full_text,created_at';
  const cDate = new Date(t.created_at);

  for (const k of keys.split(',')) {
    p[k] = t[k];
  }

  p.epochDate = cDate.valueOf();
  p.year = cDate.getFullYear();
  p.month = cDate.getMonth() + 1;
  p.day = cDate.getDate();

  p.original_tweet = t;
  return p;
};

const processedTweets = (tweets) => {
  const corpus = tweets
    .sort(chronTweets)
    .map(presenter);
  return corpus;
};

const grouper = token => (coll) => {
  const s = {};

  coll.reduce((memo, t) => {
    if (t[token] in memo) {
      memo[t[token]].push(t);
    } else {
      memo[t[token]] = [t];
    }
    return memo;
  }, s);

  return s;
};

const statsify = (o) => {
  for (const year in o) {
    fs.mkdirSync(`${pathPrefix}/${year}`);
    for (const month in o[year]) {
      fs.mkdirSync(`${pathPrefix}/${year}/${humanize(month)}`);
      for (const day in o[year][month]) {
        fs.mkdirSync(`${pathPrefix}/${year}/${humanize(month)}/${humanize(day)}`);
        for (const tweet of o[year][month][day]) {
          const path = `${year}-${humanize(month)}-${humanize(day)}-${tweet.id_str}.tweet.json`;
          const fp = `${pathPrefix}/${year}/${humanize(month)}/${humanize(day)}/${path}`;
          fs.writeFile(fp, JSON.stringify(tweet.original_tweet), (err) => {
            if (err) throw err;
            console.log(`Wrote ${fp}`);
          });
        }
      }
    }
  }
};


const regroupByYMD = (tweets) => {
  const tw = {};

  const byYear = grouper('year')(tweets);

  for (const year in byYear) {
    tw[year] = grouper('month')(byYear[year]);

    for (const month in tw[year]) {
      const byDay = grouper('day')(tw[year][month]);
      tw[year][month] = byDay;

      for (const day in byDay) {
        tw[year][month][day] = tw[year][month][day].sort((a, b) => a.epochDate - b.epochDate);
      }
    }
  }
  return tw;
};

const sanitizeData = (dirty) => {
  const bracketPos = dirty.indexOf('[');
  const clean = dirty.slice(bracketPos);
  return clean;
};

try {
  fs.mkdirSync(pathPrefix);
} catch (e) {
  if (!e.code === 'EEXIST') {
    console.error(e.code);
    process.exit(1);
  }
}

fs.readFile(fileName, 'utf8', (err, data) => {
  const tweets = processedTweets(JSON.parse(sanitizeData(data)));
  statsify(regroupByYMD(tweets));
});
