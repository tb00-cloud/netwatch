<template>
  <div class="target-page">
    <div class="header">
      <div class="title">{{ targetData.name }}</div>
      <div class="filter-container">
        <div v-if="query.relative == 'range'" class="stack">
          <p class="label">From</p>
          <input
            class="from-date"
            type="datetime-local"
            v-model="query.userFrom"
          />
        </div>
        <div v-if="query.relative == 'range'" class="stack">
          <p class="label">To</p>
          <input class="to-date" type="datetime-local" v-model="query.userTo" />
        </div>
        <div class="stack">
          <p class="label">Ago</p>
          <select v-model="query.relative" class="relative">
            <option value="range">Range</option>
            <option value="1">1h</option>
            <option value="2">2h</option>
            <option value="4">4h</option>
            <option value="6">6h</option>
            <option value="12">12h</option>
            <option value="24">24h</option>
            <option value="168">1w</option>
            <option value="336">2w</option>
            <option value="672">4w</option>
          </select>
        </div>
        <div class="stack">
          <p class="label">Group by</p>
          <select v-model="granularity.user" class="granularity">
            <option value="auto">Auto</option>
            <option value="10">10s</option>
            <option value="20">20s</option>
            <option value="30">30s</option>
            <option value="60">1m</option>
            <option value="600">10m</option>
            <option value="1800">30m</option>
            <option value="3600">1h</option>
            <option value="86400">1d</option>
          </select>
        </div>
        <div class="stack">
          <p class="label">Run</p>
          <div @click="chartRefresh" class="query"><goButton /></div>
        </div>
      </div>
    </div>

    <div class="chart">
      <div v-if="loaded == false" class="holding">{{ holdingText }}</div>
      <LineChartGenerator
        v-if="loaded"
        :chart-options="chartOptions"
        :chart-data="chartData"
        chart-id="chart"
        dataset-id-key="chart"
        :height="180"
        :styles="chartStyles"
      />
    </div>
  </div>
</template>

<script>
import goButton from "@/components/common/goButton";
import { http } from "@/services/axios.service";
import { showToast } from "@/services/toast.service";
import { Line as LineChartGenerator } from "vue-chartjs/legacy";
import {
  Chart as ChartJS,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  CategoryScale,
  PointElement,
} from "chart.js";

ChartJS.register(
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  CategoryScale,
  PointElement
);

export default {
  data() {
    return {
      holdingText: "Loading...",
      chartData: {
        labels: [null],
        datasets: [
          {
            label: null,
            backgroundColor: "#5171a5",
            data: [null],
          },
        ],
      },
      chartOptions: {
        scales: {
          y: {
            min: 0,
            max: 2,
          },
        },
      },
      chartStyles: {
        fontFamily: "Lato, sans-serif",
        width: "90%",
      },
      targetData: {
        id: null,
        name: null,
        host: null,
        port: null,
        retention: null,
        interval: null,
        enabled: null,
      },
      loaded: false,
      granularity: {
        user: "auto",
        duration: null,
      },
      query: {
        relative: "1",
        userFrom: null,
        userTo: null,
        calcFrom: null,
        calcTo: null,
      },
    };
  },
  components: {
    LineChartGenerator,
    goButton,
  },
  created() {},
  mounted() {
    this.chartRefresh();
  },
  methods: {
    async chartRefresh() {
      if (!this.validateQueryRange()) {
        return;
      }
      this.loaded = false;
      this.setQueryRange();
      let history = await this.getData(this.$route.params["id"]);

      if (history.length > 0) {
        this.processData(history);
        this.loaded = true;
      } else {
        this.holdingText = "No target history to show.";
      }
    },
    validateQueryRange() {
      if (this.query.relative == "range" && this.query.userFrom == null) {
        showToast("From is required when querying a time range", "error");
        return false;
      }
      if (this.query.relative == "range" && this.query.userTo == null) {
        showToast("To is required when querying a time range", "error");
        return false;
      }
      if (
        this.query.relative == "range" &&
        this.query.userFrom >= this.query.userTo
      ) {
        showToast("From must be before To", "error");
        return false;
      }
      return true;
    },
    setQueryRange() {
      if (this.query.relative == "range") {
        let to = new Date(this.query.userTo);
        let from = new Date(this.query.userFrom);
        this.query.calcFrom = Math.round(from.getTime() / 1000);
        this.query.calcTo = Math.round(to.getTime() / 1000);
      } else {
        let now = new Date();
        let from = new Date();

        from.setSeconds(
          from.getSeconds() - parseInt(this.query.relative) * 60 * 60
        );
        this.query.calcFrom = Math.round(from.getTime() / 1000);
        this.query.calcTo = Math.round(now.getTime() / 1000);
      }
      return;
    },
    dateDiff(from, to) {
      let diff = from.getTime() - to.getTime();
      return (diff / (1000 * 3600 * 24)).toFixed(2);
    },
    setGranularity(dayRange) {
      if (this.granularity.user == "auto") {
        if (dayRange < 1) {
          this.granularity.duration = 30;
        } else if (dayRange > 1 && dayRange <= 3) {
          this.granularity.duration = 60;
        } else if (dayRange > 3 && dayRange <= 7) {
          this.granularity.duration = 600;
        } else {
          this.granularity.duration = 3600;
        }
      } else {
        this.granularity.duration = parseInt(this.granularity.user);
        return;
      }
    },
    async getData(id) {
      try {
        const res = await http({
          target_ids: id,
          with_history: true,
          history_from: this.query.calcFrom,
          history_to: this.query.calcTo,
        }).get("targets");
        if (res.status == 200) {
          this.targetData.id = res.data[0].ID;
          this.targetData.name = res.data[0].name;
          this.targetData.host = res.data[0].host;
          this.targetData.port = res.data[0].port;
          this.targetData.retention =
            res.data[0].retentionVal +
            " " +
            res.data[0].retentionUnit.toLowerCase();
          this.targetData.interval = res.data[0].interval;
          this.targetData.enabled = res.data[0].enabled;
          this.chartData.datasets[0].label =
            this.targetData.name + " (" + this.targetData.id + ")";

          console.log(this.targetData);

          return res.data[0].history;
        }
      } catch (error) {
        if (error.response && error.response.status == 401) {
          showToast("Forbidden. Log in with a valid account", "error");
        } else {
          console.error(error);
          showToast("A server error ocurred", "error");
        }
      }
    },
    async processData(data) {
      this.chartData.labels = [];
      this.chartData.datasets[0].data = [];

      let firstTime = new Date(data[0].timestamp);
      let lastTime = new Date(data[data.length - 1].timestamp);

      let dayRange = this.dateDiff(firstTime, lastTime);

      this.setGranularity(dayRange);

      for (
        let i = firstTime;
        i < lastTime;
        i.setSeconds(i.getSeconds() + this.granularity.duration)
      ) {
        let previous = new Date(i);
        previous.setSeconds(previous.getSeconds() - this.granularity.duration);

        const filtered = data
          .filter((item) => {
            let timestamp = new Date(item.timestamp);
            return timestamp > previous && timestamp <= i;
          })
          .map((data) => data.outcome);

        this.chartData.datasets[0].data.push(
          filtered.reduce((a, b) => a + b) / filtered.length
        );

        this.chartData.labels.push(i.toLocaleString("en-GB"));
      }
    },
  },
};
</script>
<style lang="scss" scoped>
.target-page {
  .header {
    display: flex;
    justify-content: space-between;

    .title {
      font-size: xx-large;
      font-weight: 400;
      font: $primaryFont;
      display: flex;
      padding: 2rem 0 0 4rem;
      width: 10%;
    }

    .filter-container {
      font-size: x-large;
      font-weight: 400;
      font: $primaryFont;
      display: flex;
      justify-content: flex-end;
      align-items: center;
      padding: 2rem 2.8rem 0 0;
      width: 90%;

      .stack {
        text-align: left;
        height: 2.8rem;

        .label {
          font-size: small;
          margin: 0.1rem;
          padding: 0 0 0.5rem 0.5rem;
          height: 1rem;
        }

        .from-date {
          font-family: Lato, sans-serif;
          color: $primaryFont;
          width: 12rem;
          margin-left: 0.5rem;
          height: 1.6rem;
          background: $offWhite;
          border: 0;
          border-radius: 0.2rem;
          padding: 0.2rem 0.2rem 0.2rem 0.4rem;
          box-shadow: $elementShadow;
        }

        .to-date {
          font-family: Lato, sans-serif;
          color: $primaryFont;
          width: 12rem;
          margin-left: 0.5rem;
          height: 1.6rem;
          background: $offWhite;
          border: 0;
          border-radius: 0.2rem;
          padding: 0.2rem 0.2rem 0.2rem 0.4rem;
          box-shadow: $elementShadow;
        }

        .granularity {
          font-family: Lato, sans-serif;
          color: $primaryFont;
          width: 5rem;
          margin-left: 0.5rem;
          height: 2rem;
          background: $offWhite;
          border: 0;
          border-radius: 0.2rem;
          padding: 0 0.2rem 0 0.4rem;
          box-shadow: $elementShadow;
        }

        .relative {
          font-family: Lato, sans-serif;
          color: $primaryFont;
          width: 5rem;
          margin-left: 0.5rem;
          height: 2rem;
          background: $offWhite;
          border: 0;
          border-radius: 0.2rem;
          padding: 0.2rem 0.2rem 0.2rem 0.4rem;
          box-shadow: $elementShadow;
        }

        .query {
          padding: 0.2rem 0.2rem 0.2rem 0.4rem;
          width: 2rem;
        }
      }
    }
  }

  .chart {
    width: 100%;
    display: flex;
    justify-content: center;
    padding-top: 5rem;

    .holding {
      color: $primaryFont;
      height: 200px;
      display: flex;
      align-items: center;
    }
  }
}
</style>
